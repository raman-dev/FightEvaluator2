import scrapy
from scrapy.http import HtmlResponse
#what do i  want to do?
"""

     requirements
     	django launch scrapy crawler in seperate process
		receive results in django main process seperate thread
"""

class MySpider(scrapy.Spider):
    name="multiSpider"
    start_urls = ["http://ufcstats.com/statistics/events/completed"]
	
    def parse(response: HtmlResponse):
        print(response.headers)


#do what here create a seperate process that starts scrapy and uses scrapy
