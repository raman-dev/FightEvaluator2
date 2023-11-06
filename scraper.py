import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import main
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

EVENTS_URL = "http://ufcstats.com/statistics/events/completed"
#use tapology website its better and more comprehensive
EVENTS_URL2 = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
domain = "https://www.tapology.com"

DRIVER_PATH='chromedriver-win64/chromedriver'
options = Options()
options.add_argument("--headless=new")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

def extractLinkAndDate(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    """

        table.fcLeaderboard
            tr <---- column names
            tr <---- event info
                td <--- event name and link just need link for now
                td
                td  <--- event date format is YYYY.MM.DD
                td
                td
    """
    table = soup.find('table',class_='fcLeaderboard')
    # print(table.tbody)
    today = datetime.now().date()
    rows = table.findAll('tr')
    result = {'link':'','date':None}
    for i,row in enumerate(rows):
        if i == 0:
            continue
        data = row.findAll('td')
        #get href value from data object
        data_link = data[0].a['href']
        #get date from data object
        data_date = datetime.strptime(data[2].text.strip(),"%Y.%m.%d").date()
        #compare today and date when the distance from today and date increases break loop
        if data_date < today:
            break
        result['link'] = domain + data_link
        result['date'] = data_date
    return result


def getNextEvent2(url):
    linkAndDate = extractLinkAndDate(EVENTS_URL2)
    print(linkAndDate)
    # page = requests.get(linkAndDate['link'])
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(10)
    browser.get(linkAndDate['link'])
    
    source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(source, 'html.parser')
    #extract event title and matchups from page
    matchups = soup.find('ul',class_='fightCard')
    print(matchups)

# getNextEvent2(EVENTS_URL2)

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