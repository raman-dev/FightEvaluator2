import scrapy
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerProcess

import re
import unicodedata
import time
import multiprocessing
import threading
import queue
import enum 

from multiprocessing import Process

from datetime import datetime
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
    

domain = "https://www.tapology.com"
SPIDER_DOWNLOAD_DELAY_S = 15#wait 15 seconds between downlaod requests to same domain
def normalizeString(string):
    return unicodedata.normalize('NFD',string).encode('ascii', 'ignore').decode("ascii").lower()


def scrapeFighterNameAndLink(element,result_only=False):
    fighterPQ = pq(element)
    
    atag = fighterPQ('[class*="link-primary-red"]').eq(0)
    name = normalizeString(atag.text())
    
    if result_only == True:
        isWinner = False
        for span in fighterPQ("span"):
            if "Up to" in pq(span).text():
                isWinner = True
                break
        return {'name':name,'isWinner':isWinner}
    
    link = atag.attr('href')
    return {'name':name,'link':domain + link}

def scrapeWeightlbs(s: str):
    #grab a 3 digit number from string
    weightPattern = re.compile('(1|2)[0-9][0-9]')
    match = weightPattern.search(s)
    if match:
        return int(match.group(0))
    return None

def scrapePrelimStatus(s: str):
    isPrelimPattern = re.compile('Prelim')
    if isPrelimPattern.search(s):
        return True
    return False

def scrapeRounds(s: str):
    roundsPattern = re.compile('(3|5) x 5')
    match = roundsPattern.search(s)
    if not match:
        return None
    return int(match.group(0).split()[0])


def scrapeMatchups(source):
    # Writing the HTML content of the parsed soup to the file
    d = pq(source)#filename="test_0.html")
    #d -> $ in jquery
    ul = d("#sectionFightCard > ul") #this returns pyquery object
    matchups = []
    for li in ul("li"):
        #li is of type lxml.html.HtmlElement
        matchup = {}

        # dataBoutWrapper = pq(li)("div[data-bout-wrapper]").children()[0]
        dataBoutWrapper = pq(li)("div[data-bout-wrapper]:first")
        children = pq(dataBoutWrapper).children()
        # print(pq(children))
        
        dataParent = children[0]
        if len(children) == 3:
            dataParent = children[1]

        fighter_a,boutInfo,fighter_b = pq(dataParent).children()
        
        x = scrapeFighterNameAndLink(fighter_a)
        y = scrapeFighterNameAndLink(fighter_b)
        matchup['fighters_raw'] = [x,y]
        m = pq(boutInfo).text()
        #if contains 5 x 5 -> 5 rounder
        #if contains Prelim -> on prelims else on main card
        #check for an int that is valid 115,125,135,145,155,170,185,205,265
        isRumoured = re.compile('Prelim|Main Card|Co-Main|Main Event')
        if not isRumoured.search(m):
            #not a valid matchup # print(m)
            continue
        #grab prelimStatus
        isPrelim = scrapePrelimStatus(m)
        #grab the weightclass
        weightlbs = scrapeWeightlbs(m)
        #grab rounds
        rounds = scrapeRounds(m)
        if not weightlbs or not rounds:#not a valid matchup
            continue
        matchup['weight_class'] = weightlbs
        matchup['rounds'] = rounds
        matchup['isprelim'] = isPrelim
        matchups.append(matchup) 
        
    return matchups

def eventLinkParse(source: str):
    soup = BeautifulSoup(source, 'html.parser')
    table = soup.find('table',class_='fcLeaderboard')
    # print(table.tbody)
    today = datetime.now().date()
    rows = table.findAll('tr')
    result = {'link':'','date':None}
    for i,row in enumerate(rows):
        if i == 0:
            continue
        data = row.findAll('td')
        #get href value from data object
        data_event_title = data[0].a.text.strip()
        #skip non fight nights and non ppvs
        if re.search(r'(UFC\s+([0-9]+))|UFC\s+Fight\s+Night',data_event_title) == None:
            # print(data_event_title,'not a ufc event')
            continue
        data_link = data[0].a['href']
        #get date from data object
        data_date = datetime.strptime(data[2].text.strip(),"%Y.%m.%d").date()
        #compare today and date when the distance from today and date increases break loop
        # print(data_event_title,data_date)
        if data_date < today:
            break
        result['link'] = domain + data_link
        result['date'] = str(data_date)
    # print(result)
    return result


def startCrawlerProcess(spider: scrapy.Spider):
    if spider == None:
        raise ValueError("Spider cannot be None")

    print("starting CrawlerProcess")
    process = CrawlerProcess(
        settings={
            "DOWNLOAD_DELAY": SPIDER_DOWNLOAD_DELAY_S, #Delay between requests
            "LOG_LEVEL": "ERROR" 
        }
    )

    process.crawl(spider)
    process.start()
    process.join()
    return spider.results

class EventLinkSpider(scrapy.Spider):
    name = "eventLinkSpider"
    start_urls = [
        "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
    ]
    results = []

    def parse(self, response: scrapy.http.HtmlResponse):
        self.results.append(eventLinkParse(response.text))

class EventResultsSpider(scrapy.Spider):
    name = "eventResultLinkSpider"
    start_urls = []
    results = []

    def parse(self, response: HtmlResponse):
        result = self.scrapeResults(response.text)
        self.results.append(result)
    
    def scrapeResults(self,source):
        # d = pq(filename="results_test.html",encoding='utf-8')
        d = pq(source)
        ul = d("#sectionFightCard > ul") #this returns pyquery object
        matchupResults = []
        for i,li in enumerate(ul("li")):
            #li is of type lxml.html.HtmlElement
            # dataBoutWrapper = pq(li)("div[data-bout-wrapper]").children()[0]
            dataBoutWrapper = pq(li)("div[data-bout-wrapper]:first")
            children = pq(dataBoutWrapper).children()
            # print(pq(children))
            methodDataParent,resultDataParent,_ = children
            methods = []
            for span in pq(methodDataParent)("span"):
                methods.append(pq(span).text())
            
            _,method,roundTimes = methods
            fighter_a,_,fighter_b = pq(resultDataParent).children()
            
            x = scrapeFighterNameAndLink(fighter_a,result_only=True)
            y = scrapeFighterNameAndLink(fighter_b,result_only=True)

            result = {
                'fighters':[x,y]
            }
            
            #non decision fromat is M:SS Round x of y
            #decision is full time
            method = method.split(",")[0].lower()
            if 'decision' in method: 
                result['method'] = 'decision'
            elif 'ko/tko' in method:
                result['method'] = 'ko'
            elif 'submission' in method:
                result['method'] = 'submission'
            elif 'draw' in method:
                result['method'] = 'draw'
            else:
                result['method'] = 'no contest'
            
            # print(roundTimes,result['method'],method)
            if result['method'] == 'decision' or result['method'] == 'draw':
                #rounds = 3 or 5
                #time  = 15:00 or 25:00
                if "15:00" in roundTimes:
                    result['final_round'] = '3'
                else:
                    result['final_round'] = '5'#last round of fight
                result['time'] = '5:00' #final round time
            else:
                #format is Round X of Y
                #M:SS Round X of Y
                timeMatch = re.search(r'[0-5]\:[0-5][0-9]',roundTimes)
                roundMatch = re.search(r'Round [1-5] of [1-5]',roundTimes)
                result['time'] = timeMatch.group(0)
                result['final_round'] = re.search(r'[1-5]',roundMatch.group(0)).group(0)
            # print(result)
            matchupResults.append(result)
        return matchupResults

class MatchUpSpider(scrapy.Spider):
    name="matchupSpider"
    start_urls=[]
    results = []
    def parse(self, response: scrapy.http.HtmlResponse):
        title = response.css('h2::text').get()
        matchups = scrapeMatchups(response.text)
        self.results.append({
            'title':title,
            'matchups':matchups
        })

class FighterDataSpider(scrapy.Spider):
    name="fighterDataSpider"
    start_urls = []
    results = []

    def parse(self,response: scrapy.http.HtmlResponse):
        fighterData = self.scrapeFighter(response.text)
        self.results.append({response.url:fighterData})
    
    def scrapeFighter(self,source: str):
        soup = BeautifulSoup(source,'html.parser')
        
        fighterNameRecord = soup.find_all('div',class_='leading-tight')
        nameElement,recordElement = fighterNameRecord
        full_name = normalizeString(nameElement.text.strip())

        record = recordElement.text.strip().split('-')
        # print(record)
        wins = int(record[0])
        losses = int(record[1])
        draws = int(record[2])
        
        names = list(map(lambda x: x.lower(),full_name.split(' ')))
        name_index = "-".join(names)
        print('parsing => ',full_name,name_index)

        first_name = names[0]
        last_name = " ".join(names[1:])#full_name.split(' ')[-1]

        fighterData = {}
        fighterData['first_name'] = first_name
        fighterData['last_name'] = last_name
        fighterData['wins'] = wins
        fighterData['losses'] = losses
        fighterData['draws'] = draws
        fighterData['name_index'] = name_index
        
        fighterDetails = soup.find('div',id='standardDetails')
        self.scrapeFighterDetails(str(fighterDetails),fighterData)
        return fighterData
    
    def scrapeFighterDetails(self,fighterDetailsDiv,fighterData) -> dict:
        data = []
        result = pq(fighterDetailsDiv)("span")
        n = len(result)
        for i in range(0,n - 1):
            data.append(pq(result[i]).text())
        """
    0 'Gabriel Miranda' : name 
    1 'Fly' : nickname
    2 '17-6-0 (Win-Loss-Draw)' : record
    3 '1 Win': streak
    4 '34'   : age
    5 '1990 Mar 25': date-of-birth
    6 '5\'11" (180cm)' : height
    7 '71.0" (180cm)': reach
    8 'Featherweight' : weightclass
    9 '145.0 lbs': last weigh-in
        'Astra Fight Team'
        'September 09, 2023 in UFC'
        '$0 USD'
        'Telêmaco Borba, Paraná, Brazil' 
        
        2025-08-10 new query result structure
        0 name
        1 nickname
        2 record
        3 streak
        4 
        
        
        """
        height_pattern = re.compile(r"(\d)'(\d{1,2})\"\s+\(\d{3}cm\)")
        dob_pattern = re.compile(r"(\d{4})\s+(\w{3})\s+(\d{1,2})")
        reach_pattern = re.compile(r"((\d{2}\.\d+)|(\d{2}))\"\s+\(\d{3}cm\)")

        print(data)
        weightClassSet = set(["n/a","atomweight","strawweight","flyweight","bantamweight","featherweight","lightweight","welterweight","middleweight","light_heavyweight","heavyweight","catch_weight"])
        # height_string = data[6]
        #3 height values if both feet'inch" and cm are present
        #1 height value if only cm is present
        fighterData['height'] = 0
        fighterData['reach'] = 0
        fighterData['date_of_birth'] = 'N/A'
        fighterData['weight_class'] = 'lightweight'
        for d in data:
            weight_class = d.replace(" ","_").lower()
            height_match = re.search(height_pattern,d)#try feet'inch"
            reach_match = re.search(reach_pattern,d)
            dob_match = re.search(dob_pattern,d)
            # height_inches = 0
            # if len(height_match) == 1:
            #     height_inches = math.floor(int(height_match[0]) / 2.54)
            # if len(height_match) > 1:
            #     height_inches = int(height_match[0])*12 + int(height_match[1])
            if height_match:
                feet, inches = map(int, height_match.groups())
                height_inches = feet * 12 + inches
                fighterData['height'] = height_inches
            elif reach_match:
                reach_val = float(reach_match.group(1))
                reach_inches = int(round(reach_val))
                fighterData['reach'] = reach_inches
            elif weight_class != 'n/a' and  weight_class in weightClassSet:
                fighterData['weight_class'] = weight_class.upper()#first lower to query then upper to reference wtf
            elif dob_match:
                print('dob_string', d)
                dob = datetime.strptime(d, "%Y %b %d").date()
                fighterData['date_of_birth'] = dob


def FightEventSpiderProcess(q: multiprocessing.Queue):
    print("FightEventSpiderProcess starting...")
    startCrawlerProcess(EventLinkSpider)
    q.put([item for item  in EventLinkSpider.results])


def MatchUpSpiderProcess(eventLink: str,q: multiprocessing.Queue):
    print("MatchUpSpiderProcess starting...")
    MatchUpSpider.start_urls.append(eventLink)
    startCrawlerProcess(MatchUpSpider)
    q.put([item for item in MatchUpSpider.results])

def FighterDataSpiderProcess(links: list, q: multiprocessing.Queue):
    print("FighterDataSpiderProcess starting...")
    linkIndexMap = {}
    for index,link in links:
        linkIndexMap[link] = index
        FighterDataSpider.start_urls.append(link)

    startCrawlerProcess(FighterDataSpider)
    
    if len(linkIndexMap) == 1:
        result = FighterDataSpider.results[0]
        #returns a dict link:fighterData
        q.put([next(iter(result.values()))])
    else:
        #multi fetch need to organize data into a list
        resultList = []
        for result in FighterDataSpider.results:
            link,fighterData = next(iter(result.items()))
            
            resultList.append({
                'matchup-index':linkIndexMap[link],
                'fighterData':fighterData
            })
        q.put(resultList)

def FightEventResultsSpiderProcess(link: str,q: multiprocessing.Queue):
    print("FightEventResultsSpiderProcess starting...")
    EventResultsSpider.start_urls.append(link)
    startCrawlerProcess(EventResultsSpider)
    q.put([item for item  in EventResultsSpider.results])

def launchScrapyProcess(spiderProcessFunc,**kwargs):
    p = Process(target=spiderProcessFunc,kwargs=kwargs)
    p.start()
    p.join()#will wait 


def runScrapyFetchFighter(result_q: queue.Queue,link: str):
    ipc_q = multiprocessing.Queue()
    t = threading.Thread(target=launchScrapyProcess,args=(FighterDataSpiderProcess,),kwargs={'q':ipc_q,'links':[(-1,link)]})
    t.start()
    t.join()

    result = ipc_q.get()[0]

    result_q.put(result)


def runScrapyFetchFighterMulti(result_q: queue.Queue,linkList: list):
    ipc_q = multiprocessing.Queue()
    links = []
    for data in linkList:
        index,link = data.values()
        links.append((index,link))
    # print(linkList)
    t = threading.Thread(
        target=launchScrapyProcess,
        args=(FighterDataSpiderProcess,),
        kwargs={'q':ipc_q,'links':links})
    t.start()
    t.join()

    result = ipc_q.get()
    result_q.put(result)

def runScrapyFetchEvent(result_q: queue.Queue):
    #necessary since scrapy needs to use its own process
    #and only works in the main thread 
    ipc_q = multiprocessing.Queue()

    t = threading.Thread(target=launchScrapyProcess,args=(FightEventSpiderProcess,),kwargs={'q':ipc_q})
    #kwargs must be one to one mapping to keyword arguments
    #keys can only be missing if and only if function has default values in signature
    t.start()
    t.join()#block until done

    results = ipc_q.get()
    fightEventData = results[0]

    time.sleep(15)#wait 15 seconds before making another request
    print(fightEventData)
    t = threading.Thread(target=launchScrapyProcess,args=(MatchUpSpiderProcess,),
                         kwargs={'eventLink':fightEventData['link'],'q':ipc_q})
    t.start()
    t.join()#block until done
    matchupResults = ipc_q.get()[0]
    fightEventData['title'] = matchupResults['title']
    matchups = matchupResults['matchups']
    for m in matchups:
    #     #create index key from name
        for fighterData in m['fighters_raw']:
            name,link = fighterData.values()
            print(name,link)
    
    #
    result_q.put({
        'event':fightEventData,
        'matchups': matchups
    })

def runScrapyFetchResults(result_q: queue.Queue,link: str):
    ipc_q = multiprocessing.Queue()

    t = threading.Thread(target=launchScrapyProcess,args=(FightEventResultsSpiderProcess,),kwargs={'q':ipc_q,'link':link})
    #kwargs must be one to one mapping to keyword arguments
    #keys can only be missing if and only if function has default values in signature
    t.start()
    t.join()#block until done

    #always returns a list of data
    results = ipc_q.get()[0]

    result_q.put(results)