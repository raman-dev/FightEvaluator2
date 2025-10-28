from django.views.decorators.http import require_GET
from django.http import JsonResponse
import threading
import time

import scrapy
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerProcess

class TestSpider(scrapy.Spider):
    name = "testSpider"
    start_urls = [
        "http://ufcstats.com/statistics/events/completed"
    ]

    def parse(self, response: HtmlResponse):
        print(response.headers)

mThread = None

def scrapyControlFunc():
    #doesn't work because scrapy process
    #needs signal handlers which cannot be registered from non main threads
    #this is a python thing
    process = CrawlerProcess(
        settings={
            "DOWNLOAD_DELAY": 4 #Delay between requests 
        }
    )

    process.crawl(TestSpider)
    process.start()
    print("Scrapy process finished")



@require_GET
def scrapy_start(request):
    # This is a placeholder for the actual scrapy test implementation
    #launch a thread if it is not running 
    global mThread
    if mThread == None or not mThread.is_alive() : 
        mThread = threading.Thread(target=scrapyControlFunc,args=())
        mThread.start()
        return JsonResponse({'status': 'Scrapy started'})

    return JsonResponse({'status': 'Scrapy start endpoint'})


#---------------------------------------------------------------------------
def threadRunner(*args, **kwargs):
    # Placeholder for actual thread work
    print("received args:",repr(args),"\nreceived kwargs: ",repr(kwargs))
    time.sleep(10)  # Simulate long-running task
    print("Thread work completed")
    #start process crawler here

@require_GET
def scrapy_test(request):
    # This is a placeholder for the actual scrapy test implementation
    #launch a thread if it is not running 
    global mThread
    if mThread == None or not mThread.is_alive() : 
        mThread = threading.Thread(target=threadRunner,args=('hello','world'))
        mThread.start()
        return JsonResponse({'status': 'Scrapy test started'})

    return JsonResponse({'status': 'Scrapy test endpoint reached'})