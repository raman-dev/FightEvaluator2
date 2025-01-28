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

    sportsbookTable = pq(page('.sportsbook-table'))[0]
    # print(sportsbookTable)
    prev = None
    result = []
    for i,tableRow in enumerate(pq(sportsbookTable)('tr')):
        if i == 0:
            continue
        tr = pq(tableRow)
        # print(tr)
        name = tr('div.event-cell__name').text()
        odd = tr('td:last-child').text()
        # print(name,odd)
        newOdd = (name,odd)
        if not prev:
            prev = newOdd
            continue
        #pair the 2 fighter odds together
        result.append((prev,newOdd))
        prev = None

    return result
        
