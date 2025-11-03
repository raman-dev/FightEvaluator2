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

domain = "https://www.tapology.com"
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
        print(data_event_title,data_date)
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