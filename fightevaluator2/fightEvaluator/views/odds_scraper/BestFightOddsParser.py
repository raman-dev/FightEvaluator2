from pyquery import PyQuery as pq
from typing import *

"""

    structure

    .sportsbook-table
    
        tr
            th
                event-cell__name-text <--contains name
            td: last-child
                span <--contains outcome

"""

def parseOdds(source) -> List:
    
    page = pq(source)
    table = None
    # print(page('.table-div'))
    for i,tableContainer in enumerate(pq(page('.table-div'))):
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
    """ 
    # print(table)
    result = []
    curr = {}
    prev = None
    for i,tr in enumerate(pq(table)('tbody tr')):
        #if tr has class pr skip over
        tr_pq = pq(tr)
        if tr_pq.hasClass('pr'):
            continue
        print(tr)
        
    return result
        