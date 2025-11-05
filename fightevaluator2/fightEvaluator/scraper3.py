import scrapy
import multiprocessing
from scrapy.crawler import CrawlerProcess

from .scraper import eventLinkParse,EVENTS_URL2
from .scraper2 import scrapeMatchups

def printProcessInfo(sleep=None):
    if sleep != None:
        time.sleep(sleep)
    print("==== Process Info ====")
    print("current.process => ", multiprocessing.current_process().name)
    print("current.process.id => ", multiprocessing.current_process().pid)
    print("current.thread => ",threading.current_thread().name)
    print("======================")

class EventLinkSpider(scrapy.Spider):
    name = "eventLinkSpider"
    start_urls = [
        EVENTS_URL2
    ]
    results = []

    def parse(self, response: scrapy.http.HtmlResponse):
        self.results.append(eventLinkParse(response.text))


class MatchUpSpider(scrapy.Spider):
    name="matchupSpider"
    start_urls= []
    results = []

    def parse(self, response: scrapy.http.HtmlResponse):
        title = response.css('h2::text').get()
        matchups = scrapeMatchups(response.text)
        self.results.append({
            'title':title,
            'matchups':matchups
        })

def startCrawlerProcess(spider: scrapy.Spider):
    if spider == None:
        raise ValueError("Spider cannot be None")
    process = CrawlerProcess(
        settings={
            "DOWNLOAD_DELAY": 10, #Delay between requests
            "LOG_LEVEL": "ERROR" 
        }
    )

    process.crawl(spider)
    process.start()
    return spider.results

def FightEventSpiderProcess(q: multiprocessing.Queue):
    startCrawlerProcess(EventLinkSpider)
    q.put([item for item  in EventLinkSpider.results])


def MatchUpSpiderProcess(eventLink: str,q: multiprocessing.Queue):
    MatchUpSpider.start_urls.append(eventLink)
    startCrawlerProcess(MatchUpSpider)

    q.put([item for item in MatchUpSpider.results])

def launchScrapyProcess(spiderProcessFunc,**kwargs):
    p = multiprocessing.Process(target=spiderProcessFunc,kwargs=kwargs)
    p.start()