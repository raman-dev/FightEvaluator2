from .fetcher import Fetcher
from . import DraftKingsParser,BestFightOddsParser
from rich import print as rprint
from rich.table import Table
from rich.console import Console
import json
import datetime
import os
from pathlib import Path
from typing import *

from enum import Enum
from abc import abstractmethod
from pyquery import PyQuery as pq
from typing import *

console = Console()
dk_url = 'https://sportsbook.draftkings.com/leagues/mma/ufc'
bestfightodds_url = 'https://www.bestfightodds.com'


"""

SHOULD IMPLEMENT IN SUCH A WAY WITH A FACTORY METHOD THAT 
RETURNS PARSERS FOR PARTICULAR SITES

"""

# class Parser:
#     def __init__(self,url):
#         self.url = url
    
#     @abstractmethod
#     def parseOdds(self,source) -> List:
#         pass

# class BestFightOddsParser(Parser):
#     def parseOdds(self,source) -> List:
#         page = pq(source)
#         table = None
#         for _,tableContainer in enumerate(pq(page('.table-div'))):
#             title = pq(tableContainer)('.table-header h1').text()
#             if "UFC" in title:
#                 table = pq(tableContainer)('.odds-table')
#                 break
#         result = []
#         curr = []
#         prev = None
#         for _,tr in enumerate(pq(table)('tbody tr')):
#             # if tr has class pr skip over
#             tr_pq = pq(tr)
#             if tr_pq.hasClass('pr'):
#                 continue
#             name = tr_pq('th span').text()
#             odds = []
#             for _,td in enumerate(tr_pq('td.but-sg')):
#                 odds.append(pq(pq(td)('span')[0]).text())
            
#             if odds == []:
#                 continue
#             curr.append([name,odds])
#             if prev != None:
#                 result.append(curr)
#                 curr = []
#                 prev = None
#             else:
#                 prev = curr
#         return result



def getOddsFromFile():
    oddsJson = None
    oddsList = []
    url= None
    with open("fightEvaluator/views/odds_scraper/odds.json","r",encoding="ascii") as oddsFile:
        oddsJson = json.load(oddsFile)
        rprint('Reading from file...')
        oddsList = oddsJson['odds']
        url = oddsJson['url']
    
    # rprint('site',url)
    n = len(oddsList)
    if url == dk_url:
        for i in range(0,n):
            _,_,a,b = oddsList[i]
            if a[0] == '\u2212':
                oddsList[i][2] = -int(a[1:])
            else:
                oddsList[i][2] = int(a)
            if b[0] == '\u2212':
                oddsList[i][3] = -int(b[1:])
            else:
                oddsList[i][3] = int(b)
        # print(oddsList[i][2],type(oddsList[i][2]))
    table = Table(title="Odds",show_lines=True)
    

    table.add_column('fighter_a',vertical="middle",justify="center")
    table.add_column('fighter_b',vertical="middle",justify="center")
    table.add_column('odds_a',vertical="middle",justify="center",style="green")
    table.add_column('odds_b',vertical="middle",justify="center",style="green")

    for fighter_a,fighter_b,oddsA,oddsB in oddsList:
        table.add_row(fighter_a,fighter_b,str(oddsA),str(oddsB))
    console.print(table)

    return oddsList

def fetchFromSite():
    # print('OS.GETCWD => ',os.getcwd())
    # print('Path.CWD() => ',Path.cwd())
    """
        read odds.json 
            if updated != today's date
                then fetch from site and parse
            else:
                read from file
        
        odds: [[fighter_a,fighter_b,odds_a,odds_b],...]
    """
    oddsJson = None
    oddsList = []
    
    # url = bestfightodds_url
    url = dk_url
    with open("fightEvaluator/views/odds_scraper/odds.json","r+",encoding="ascii") as oddsFile:
        oddsJson = json.load(oddsFile)
        rprint('Fetching from site...')
        source = ""
        with Fetcher() as fetcher:
            source = fetcher.fetch(url=url,wait_time=8)
        
        oddsRaw = []
        if url == dk_url:
            oddsRaw = DraftKingsParser.parseOdds(source)
        elif url == bestfightodds_url:
            oddsRaw = BestFightOddsParser.parseOdds(source)

        
        if url == dk_url:
            for a,b in oddsRaw:
                data = [a[0],b[0],a[1],b[1]]
                oddsList.append(data)
        else:#url == bestfightodds_url
            """
                result -> [
                    [ name0:odds,name1:odds ],
                    [ name0:odds,name1:odds],
                ]
            """
            for matchup in oddsRaw:
                # rprint(matchup)
                oa,ob = matchup
                name0,odds0 = oa
                name1,odds1 = ob
                data = [name0,name1,int(odds0[0]),int(odds1[0])]
                oddsList.append(data)
        
        oddsJson['url'] = url
        oddsJson['odds'] = oddsList

        oddsFile.seek(0)
        json.dump(oddsJson,oddsFile)
        oddsFile.truncate()
    n = len(oddsList)
    if url == dk_url:
        for i in range(0,n):
            _,_,a,b = oddsList[i]
            if a[0] == '\u2212':
                oddsList[i][2] = -int(a[1:])
            else:
                oddsList[i][2] = int(a)
            if b[0] == '\u2212':
                oddsList[i][3] = -int(b[1:])
            else:
                oddsList[i][3] = int(b)
            # print(oddsList[i][2],type(oddsList[i][2]))
    table = Table(title="Odds",show_lines=True)
    

    table.add_column('fighter_a',vertical="middle",justify="center")
    table.add_column('fighter_b',vertical="middle",justify="center")
    table.add_column('odds_a',vertical="middle",justify="center",style="green")
    table.add_column('odds_b',vertical="middle",justify="center",style="green")

    for fighter_a,fighter_b,oddsA,oddsB in oddsList:
        table.add_row(fighter_a,fighter_b,str(oddsA),str(oddsB))
    console.print(table)

    return oddsList