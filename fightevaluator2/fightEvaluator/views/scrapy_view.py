from django.views.decorators.http import require_GET
from django.http import JsonResponse
import threading
import time
import zmq
from rich import print as rprint

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

@require_GET
def zmq_client_test(request):
    global mThread
    if mThread == None or not mThread.is_alive() : 
        mThread = threading.Thread(target=clientStartTestFunction,args=())
        mThread.start()
        return JsonResponse({'status': 'Scrapy started'})

    return JsonResponse({'status': 'Scrapy start endpoint'})


DEFAULT_TIMEOUT = 5#seconds
def timeout(seconds=DEFAULT_TIMEOUT):
    return seconds * 1000

def clientStartTestFunction():
    PORT = 42069
    with zmq.Context() as context:
        with context.socket(zmq.REQ) as socket:
            
            socket.setsockopt(zmq.LINGER,0)#must be set so pending messages are 
            #discarded and when term and disconnect are called
            socket.setsockopt(zmq.SNDTIMEO,timeout(seconds=5))#send timeout
            socket.setsockopt(zmq.RCVTIMEO,timeout(seconds=5))#receive timeout

            socket.connect(f"tcp://localhost:{PORT}")
            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)
            
            try:
                socket.send_pyobj({'hello':'world'})
                event_mask = socket.poll(timeout(seconds=5))
                # if socketEvents == []:
                #     rprint(f"[bold red]No response from server within {DEFAULT_TIMEOUT} seconds.[/bold red]")
                #     socket.close()
                #     break
                # socket,event_mask = socketEvents[0]
                if (event_mask & zmq.POLLIN) != 0:
                    message = socket.recv_pyobj()
                    rprint(f"[bold green]Received reply:[/bold green] {message}")
                    # if Commands[choice] == Commands.KILL_SERVER:
                    #     rprint("Client will now close.")
                    #     break
                else:
                    rprint(f"[bold red]No response from server within {DEFAULT_TIMEOUT} seconds.[/bold red]")
                    socket.close()
            except KeyboardInterrupt:
                print("Ending client..")
           
            poller.unregister(socket)

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