import scrapy
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerProcess

import multiprocessing
from multiprocessing import Process
import threading
"""

     requirements
     	django launch scrapy crawler in seperate process
         
        scrapy process cannot be initiated from non main thread
        because scrapy needs to register signal handlers and that can only
        be done in the main thread of a process

		receive results in django main process seperate thread
"""

#Print current process name and id with thread name
def printProcessInfo():
    print("==== Process Info ====")
    print("current.process => ", multiprocessing.current_process().name)
    print("current.process.id => ", multiprocessing.current_process().pid)
    print("current.thread => ",threading.current_thread().name)
    print("======================")

class MySpider(scrapy.Spider):
    name="multiSpider"
    start_urls = ["http://ufcstats.com/statistics/events/completed"]
	
    def parse(self,response: HtmlResponse):
        printProcessInfo()
        print(response.headers)


#do what here create a seperate process that starts scrapy and uses scrapy
# if __name__ == "__main__":

def startCrawlerProcess(spider: scrapy.Spider):
    if spider == None:
        raise ValueError("Spider cannot be None")
    process = CrawlerProcess(
        settings={
            "DOWNLOAD_DELAY": 4 #Delay between requests 
        }
    )

    process.crawl(spider)
    process.start()
    print("Scrapy process finished")
    printProcessInfo()

# Example usage start a crawler process with a given spider
startCrawlerProcess(MySpider)
"""

    django_proc 
        main_thread   scrapy_result_receiver_thread
                            launch a scrapy_control_process
                                 |-----------queue------------scrapy_control_process
                                                                    launch a scrapy_crawler_process
                                                                                        |
                                                                                        --------------scrapy_crawler_process
                                                                           |---------pipe/queue------------|


"""

# def launchScrapyControlProcess():
#     p = Process(target=startCrawlerProcess, args=(MySpider))
#     p.start()
