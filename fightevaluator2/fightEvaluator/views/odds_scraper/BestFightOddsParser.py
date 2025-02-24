from pyquery import PyQuery as pq
from typing import *
from datetime import datetime
import re
    

#assume always a table to parse
"""
        result structure is what?
        {
            fname_0: odd0
            fname_1: odd1 
        }

        table
            tr
              th
              td
""" 
def convert_mmdd_suffix_to_date(month_day_suffix: str,event_date: datetime.date):
    #remove suffix from string
    """
        string format
            month  n(st/nd/th)
        
    """
    print(month_day_suffix)
    month,day = month_day_suffix.split(" ")
    day = day[:-2]
    if len(day) == 1:
        day = "0" + day
    return datetime.strptime(str(event_date.year)+" "+ month + " "+day,"%Y %B %d").date()

def parseOdds(source:str ,date: datetime.date) -> List:

    """
        convert to month number
    """
    page = pq(source)
    # table = None
    tables = []
    for _,tableContainer in enumerate(pq(page('.table-div'))):
        
        title = pq(tableContainer)('.table-header h1').text()
        if "UFC" in title:
            #check date 
            table_date = convert_mmdd_suffix_to_date(month_day_suffix=pq(tableContainer)('span.table-header-date').text(),event_date=date)
            delta_days = abs(table_date.day - date.day)
            if delta_days <= 1 and table_date.month == date.month :
                table = pq(tableContainer)('.odds-table')
                tables.append(table)
            # break
    result = []
    
    for table in tables:
        curr = []
        prev = None
        for _,tr in enumerate(pq(table)('tbody tr')):
            # if tr has class pr skip over
            tr_pq = pq(tr)
            if tr_pq.hasClass('pr'):
                continue
            name = tr_pq('th span').text()
            odds = []
            for _,td in enumerate(tr_pq('td.but-sg')):
                odds.append(pq(pq(td)('span')[0]).text())
            
            if odds == []:
                continue
            curr.append([name,odds])
            if prev != None:
                result.append(curr)
                curr = []
                prev = None
            else:
                prev = curr
    return result
        