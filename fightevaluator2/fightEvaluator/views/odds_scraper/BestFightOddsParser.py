from pyquery import PyQuery as pq
from typing import *
    

def parseOdds(source) -> List:
    page = pq(source)
    table = None
    for _,tableContainer in enumerate(pq(page('.table-div'))):
        title = pq(tableContainer)('.table-header h1').text()
        if "UFC" in title:
            table = pq(tableContainer)('.odds-table')
            break
    
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
    result = []
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
        