import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerProcess
from parser import eventLinkParse, scrapeFighterNameAndLink, scrapeMatchups, normalizeString, scrapeResults,scrapeFighter

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

def startCrawlerProcess(spider: scrapy.Spider):
    if spider == None:
        raise ValueError("Spider cannot be None")

    print("starting CrawlerProcess")
    
    # This establishes Scrapy's default logging behavior
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    settings = {
        "DOWNLOAD_DELAY": SPIDER_DOWNLOAD_DELAY_S, #Delay between requests
        "LOG_ENABLED":True,
        "HTTPERROR_ALLOW_ALL": True,
        "LOG_LEVEL": "DEBUG", #use this if scrapy itself didnt give correct response
        # "LOG_LEVEL":"ERROR",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
    }
    process = CrawlerProcess(
        settings=settings
    )

    def spiderOpenReciever(spider):
        print(f"{spider.name} spider started")
    def spiderClosedReceiver(spider):
        print(f"{spider} spider closed")

    crawler = process.create_crawler(spider)
    crawler.signals.connect(spiderOpenReciever,signal=signals.spider_opened)
    crawler.signals.connect(spiderClosedReceiver,signal=signals.spider_closed)
    process.crawl(crawler)
    print("starting crawler process")
    process.start()
    process.join()
    

    print("waiting for process")
    return spider.results

class EventLinkSpider(scrapy.Spider):
    name = "eventLinkSpider"
    start_urls = [
        "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
    ]
    handle_httpstatus_list = [403]
    results = []

    def parse(self, response: scrapy.http.HtmlResponse):
        print(response.text)
        self.results.append(eventLinkParse(response.text))

class EventResultsSpider(scrapy.Spider):
    name = "eventResultLinkSpider"
    start_urls = []
    results = []

    def parse(self, response: HtmlResponse):
        print(response.text)
        result = scrapeResults(response.text)#self.scrapeResults(response.text)
        self.results.append(result)

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
        self.results.append({response.url:fighterData})


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
    time.sleep(5)
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