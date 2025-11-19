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

class WeightClass(enum.Enum):
    NA = "n/a"
    ATOMWEIGHT = "atomweight"
    STRAWWEIGHT = "strawweight"
    FLYWEIGHT = "flyweight"
    BANTAMWEIGHT = "bantamweight"
    FEATHERWEIGHT = "featherweight"
    LIGHTWEIGHT = "lightweight"
    WELTERWEIGHT = "welterweight"
    MIDDLEWEIGHT = "middleweight"
    LIGHT_HEAVYWEIGHT = "light_heavyweight"
    HEAVYWEIGHT = "heavyweight"
    CATCH_WEIGHT = "catch_weight"
    

domain = "https://www.tapology.com"

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

def scrapeFighterDetails(fighterDetailsDiv,fighterData) -> dict:
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
    # height_string = data[6]
    #3 height values if both feet'inch" and cm are present
    #1 height value if only cm is present
    fighterData['height'] = 0
    fighterData['reach'] = 0
    fighterData['date_of_birth'] = 'N/A'
    fighterData['weight_class'] = WeightClass.LIGHTWEIGHT
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
        elif weight_class != 'n/a' and  weight_class in WeightClass:
            fighterData['weight_class'] = weight_class.upper()#first lower to query then upper to reference wtf
        elif dob_match:
            print('dob_string', d)
            dob = datetime.strptime(d, "%Y %b %d").date()
            fighterData['date_of_birth'] = dob

def scrapeFighter(source: str):
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
    scrapeFighterDetails(str(fighterDetails),fighterData)
    return fighterData

def startCrawlerProcess(spider: scrapy.Spider):
    if spider == None:
        raise ValueError("Spider cannot be None")

    print("starting CrawlerProcess")
    process = CrawlerProcess(
        settings={
            "DOWNLOAD_DELAY": 8, #Delay between requests
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
        fighterData = scrapeFighter(response.text)
        self.results.append(fighterData)

def FightEventSpiderProcess(q: multiprocessing.Queue):
    print("FightEventSpiderProcess starting...")
    startCrawlerProcess(EventLinkSpider)
    q.put([item for item  in EventLinkSpider.results])


def MatchUpSpiderProcess(eventLink: str,q: multiprocessing.Queue):
    print("MatchUpSpiderProcess starting...")
    MatchUpSpider.start_urls.append(eventLink)
    startCrawlerProcess(MatchUpSpider)
    q.put([item for item in MatchUpSpider.results])

def FighterDataSpiderProcess(fighterLink: str, q: multiprocessing.Queue):
    print("FighterDataSpiderProcess starting...")
    FighterDataSpider.start_urls.append(fighterLink)
    startCrawlerProcess(FighterDataSpider)
    q.put([item for item in FighterDataSpider.results])

def launchScrapyProcess(spiderProcessFunc,**kwargs):
    p = Process(target=spiderProcessFunc,kwargs=kwargs)
    p.start()
    p.join()#will wait 


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
    