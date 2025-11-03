import scrapy
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerProcess
import time

import multiprocessing
from multiprocessing import Process
import threading
import concurrent

"""

     requirements
     	django launch scrapy crawler in seperate process
         
        scrapy process cannot be initiated from non main thread
        because scrapy needs to register signal handlers and that can only
        be done in the main thread of a process

		receive results in django main process seperate thread
"""

#Print current process name and id with thread name
def printProcessInfo(sleep=None):
    if sleep != None:
        time.sleep(sleep)
    print("==== Process Info ====")
    print("current.process => ", multiprocessing.current_process().name)
    print("current.process.id => ", multiprocessing.current_process().pid)
    print("current.thread => ",threading.current_thread().name)
    print("======================")

class MySpider(scrapy.Spider):
    name="multiSpider"
    start_urls = ["http://ufcstats.com/statistics/events/completed"]
    results = {}
    
    def parse(self,response: HtmlResponse):
        # printProcessInfo()
        # print(response.headers)
        self.results ['headers'] = response.headers,
        self.results ['text']= response.text

#do what here create a seperate process that starts scrapy and uses scrapy
# if __name__ == "__main__":

def startCrawlerProcess(spider: scrapy.Spider):
    if spider == None:
        raise ValueError("Spider cannot be None")
    process = CrawlerProcess(
        settings={
            "DOWNLOAD_DELAY": 4, #Delay between requests
            "LOG_LEVEL": "ERROR" 
        }
    )

    process.crawl(spider)
    process.start()
    process.join()
    return spider.results
    # print("Scrapy process finished")
    # printProcessInfo()

# Example usage start a crawler process with a given spider
# startCrawlerProcess(MySpider)
"""

    django_proc 
        main_thread   scrapy_result_receiver_thread
                            launch a scrapy_control_process
                                 |-----------queue------------scrapy_control_process
                                                                    launch a scrapy_crawler_process
                                                                                        |
                                                                                        --------------scrapy_crawler_process
                                                                           |---------pipe/queue------------|


                                                                           
    working solution
        launch thread
            use processpoolexecutor perform scraping or whatever
            thread receives result
            modify db if needed to 
    
"""


# def launchScrapyProcess():
#     startCrawlerProcess(MySpider)

def launchProcess():
    p = Process(target=startCrawlerProcess,args=(MySpider,))
    p.start()
    p.join()#will wait 


def testFunc():
    printProcessInfo()
    return 456

#thread function that launches a process pool
#write 
def launchScrapyWithProcessPool():
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        # future = executor.submit(testFunc)
        future = executor.submit(startCrawlerProcess,MySpider)
        result = future.result()
        print(result)

def launchProcessFromThread():
    t = threading.Thread(target=launchScrapyWithProcessPool,args=())
    t.start()
    # t.join()


# if __name__=="__main__":
#     # launchProcess()
#     launchProcessFromThread()
#     printProcessInfo()
#     line = input("Enter something:")
#     while line != "quit":
#         print(line)
#         line = input("Enter something:")
from datetime import datetime
from bs4 import BeautifulSoup
import re
import unicodedata
from pyquery import PyQuery as pq


domain = "https://www.tapology.com"

def normalizeString(string):
    return unicodedata.normalize('NFD',string).encode('ascii', 'ignore').decode("ascii").lower()


def scrapeFighterData(element,result_only=False):
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
        
        x = scrapeFighterData(fighter_a)
        y = scrapeFighterData(fighter_b)
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
        result['date'] = data_date
    # print(result)
    return result

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

    def parse(self, response: scrapy.http.HtmlResponse):
        title = response.css('h2::text').get()
        matchups = scrapeMatchups(response.text)
        # for m in matchups:
        #     w = scraper.poundsToWeightClass(m['weight_class'])
        #     m['weight_class'] = w
        self.results.append({
            'title':title,
            'matchups':matchups
        })

def FightEventSpiderProcess(q: multiprocessing.Queue):
    startCrawlerProcess(EventLinkSpider)
    q.put([item for item  in EventLinkSpider.results])


def MatchUpSpiderProcess(eventLink: str,q: multiprocessing.Queue):
    MatchUpSpider.start_urls.append(eventLink)
    startCrawlerProcess(MatchUpSpider)

    q.put([item for item in MatchUpSpider.results])

def launchScrapyProcess(spiderProcessFunc,**kwargs):
    p = Process(target=spiderProcessFunc,kwargs=kwargs)
    p.start()
    p.join()#will wait 


def testFunction(*args,key,key0=None):
    print(*args,key)

if __name__ == "__main__":
    q = multiprocessing.Queue()

    # t = threading.Thread(target=launchScrapyProcess,args=(FightEventSpiderProcess,),kwargs={'q':q})
    t = threading.Thread(target=testFunction,kwargs={"key":"value"})
    #kwargs must be one to one mapping to keyword arguments
    #keys can only be missing if and only if function has default values in signature
    t.start()
    t.join()#block until done

    # results = q.get()
    # fightEventData = results[0]

    # t = threading.Thread(target=launchScrapyProcess,args=(Ma,q))
    # t.start()
    # t.join()#block until done
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     eventFuture = executor.submit(startCrawlerProcess,EventLinkSpider)
    #     eventResults = eventFuture.result()
    #     eventData = eventResults[0]
    #     print(eventData)

    #     MatchUpSpider.start_urls.append(eventData['link'])
    #     mFuture = executor.submit(startCrawlerProcess,MatchUpSpider)
    #     mFutureResults = mFuture.result()

    #     print(mFutureResults)