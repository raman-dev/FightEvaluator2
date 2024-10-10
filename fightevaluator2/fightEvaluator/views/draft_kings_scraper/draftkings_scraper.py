from .fetcher import Fetcher
from . import DraftKingsParser
from rich import print as rprint
from rich.table import Table
from rich.console import Console
import json
import datetime
import os
from pathlib import Path

console = Console()
dk_url = 'https://sportsbook.draftkings.com/leagues/mma/ufc'
def run():

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
    currentDate = datetime.date.today()
    with open("fightEvaluator/views/draft_kings_scraper/odds.json","r+",encoding="ascii") as oddsFile:
        oddsJson = json.load(oddsFile)
        if oddsJson['updated'] == None or datetime.datetime.strptime(oddsJson['updated'],"%Y-%m-%d").date() != currentDate:
            rprint('Fetching from site...')
            oddsRaw = DraftKingsParser.parseOdds(
                Fetcher.fetchWithRequests(dk_url))
            #save to odds.json
            
            for a,b in oddsRaw:
                data = [a[0],b[0],a[1],b[1]]
                oddsList.append(data)
            oddsJson['odds'] = oddsList
            oddsJson['updated'] = currentDate.__str__()
            
            oddsFile.seek(0)
            json.dump(oddsJson,oddsFile)
            oddsFile.truncate()
        else:
            rprint('Reading from file...')
            oddsList = oddsJson['odds']
    n = len(oddsList)
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

# run(dk_url)