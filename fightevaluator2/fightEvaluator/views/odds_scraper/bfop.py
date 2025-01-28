from BestFightOddsParser import *

from fetcher import *

source = ""
bestfightodds_url = 'https://www.bestfightodds.com'

# with open('bfop_html.html','r',encoding='utf8') as f:
    # source = f.readlines()

# print(source)

# source = Fetcher.fetchWithRequests(url=bestfightodds_url)
# with Fetcher() as fetcher:
#     source = fetcher.fetch(url=bestfightodds_url,wait_time=8)
#     with open("bfop_html.html","w+",encoding='utf8') as f:
#         f.write(source)

with open("bfop_html.html","r",encoding='utf8') as f:
    source=f.readlines()

parseOdds(source)
