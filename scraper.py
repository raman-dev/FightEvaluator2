import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import main

EVENTS_URL = "http://ufcstats.com/statistics/events/completed"

def getNextEvent(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # nextEvent = soup.find('table tbody tr td a')
    #get the second row of the first table use soup object
    table = soup.table
    """
    
        tr 
          td
            img
            i
               a  <---- contains link to event and text contains event name
               span <--contains date
          td  <---contains location
    
    """
    #always second row of table on current iteration of ufcstats.com
    nextEventRow = table.tbody.findAll('tr')[1]
    #extract the name and date and location of the event
    nameData, locationData = nextEventRow.findAll('td')
    name = nameData.i.a.text.strip()
    fdate = datetime.strptime(nameData.span.text.strip(),"%B %d, %Y").date()
    link = nameData.i.a['href']
    location = locationData.text.strip()

    return {
        "name": name,
        "date": fdate,
        "location": location,
        "link": link
    }


def getEventMatchups(event_url):
    page = requests.get(event_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # nextEvent = soup.find('table tbody tr td a')
    #get the second row of the first table use soup object
    # table = soup.find('')
    #find table by class name from soup
    tableBody = soup.find('table')
    """
        table has 10 columns
        second column is fighter names
        seventh column is weightclass

        fighter column data structure
            td 
                p 
                 a <-- contains fighter name
                p
                 a <-- contains fighter name
        weightclass column data structure
            td 
                p <-- contains matchup weightclass
    """
    #for every row in the table body
    #extract the fighter names and weightclass
    #return a list of matchups
    # print(tableBody)
    rows = tableBody.findAll('tr')
    # print(rowData)
    matchups = []
    for i,row in enumerate(rows):
        if i == 0:
            continue
        rowData = row.findAll('td')
        fa,fb = rowData[1].findAll('p')   
        weightClassData = rowData[6]

        fighter_a = fa.a.text.strip()
        fighter_b = fb.a.text.strip()
        weightclass = weightClassData.p.text.replace("Women's","").strip().upper().replace(" ","_")

        matchups.append({
            "fighter_a": fighter_a,
            "fighter_b": fighter_b,
            "weight_class": main.WeightClass[weightclass]
        })
    return matchups


# eventInfo = getNextEvent(EVENTS_URL)
# matchups = getEventMatchups(eventInfo['link'])
# print(eventInfo)
# print(getEventMatchups('http://ufcstats.com/event-details/7c4ec656d8fcb867'))
# print(getEventMatchups(eventInfo['link']))