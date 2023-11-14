import requests 
from bs4 import BeautifulSoup
from datetime import datetime
from models import WeightClass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time,re,json,os
import unicodedata


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


def toWeightClass(weight):
    #switch statement
    if weight == 115:
        return WeightClass["STRAWWEIGHT"]
    elif weight == 125:
        return WeightClass["FLYWEIGHT"]
    elif weight == 135:
        return WeightClass["BANTAMWEIGHT"]
    elif weight == 145:
        return WeightClass["FEATHERWEIGHT"]
    elif weight == 155:
        return WeightClass["LIGHTWEIGHT"]
    elif weight == 170:
        return WeightClass["WELTERWEIGHT"]
    elif weight == 185:
        return WeightClass["MIDDLEWEIGHT"]
    elif weight == 205:
        return WeightClass["LIGHT_HEAVYWEIGHT"]
    elif weight == 265:
        return WeightClass["HEAVYWEIGHT"]
    else:
        return WeightClass["CATCH_WEIGHT"]

def getNextEvent2():
    linkAndDate = extractLinkAndDate(EVENTS_URL2)
    print(linkAndDate)
    # page = requests.get(linkAndDate['link'])
    browser = webdriver.Chrome(options=options)
    # browser.implicitly_wait(10)
    browser.get(linkAndDate['link'])
    
    source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(source, 'html.parser')
    #extract event title and matchups from page
    matchupsRaw = soup.find('ul',class_='fightCard')
    """
        div.eventPageHeaderTitles.h1 <-- event title
        ul.fightCard
            li.fightCard
                div.fightCardBout id=someId
                    fightCardFighterBout left/right
                        a <--fighter link
                        a.textContent <-- fighter name
                    fightCardMatchup
                        td.textContent <--rounds
                            fightCardWeight.span <--weightclass
                        

    """
    eventName = soup.find('div',class_='eventPageHeaderTitles').h1.text.strip()
    titleUl = soup.select('div.details ul.clearfix')[0]
    # print(titleUl.findAll('li'))
    location = titleUl.findAll('li')[5].span.text.strip()
    matchups = []
    for li in matchupsRaw.findAll('li'):
        # print(li)
        fightCardBout = li.find('div',class_='fightCardBout')
        fighter_a = fightCardBout.find('div',class_='fightCardFighterBout left')
        fighter_b = fightCardBout.find('div',class_='fightCardFighterBout right')
        fightCardMatchup = fightCardBout.find('div',class_='fightCardMatchup')
        rounds = fightCardMatchup.find('td').text.strip()
        weightclass = fightCardMatchup.find('span',class_='weight').text.strip()
        a = {
            'name': fighter_a.a.text.strip(),
            'link': fighter_a.a['href']
        }
        b = {
            'name': fighter_b.a.text.strip(),
            'link': fighter_b.a['href']
        }
        matchups.append({
            'fighter_a':a['name'],
            'fighter_b':b['name'],
            'fighter_a_link':a['link'],
            'fighter_b_link':b['link'],
            'rounds':rounds,
            'weight_class':toWeightClass(int(weightclass))
        })
    # print(matchups)

    return {'event':{'name':eventName,'date':linkAndDate['date'],'location':location},'matchups':matchups}

# print(getNextEvent2())

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
            "weight_class": WeightClass[weightclass]
        })
    return matchups


# eventInfo = getNextEvent(EVENTS_URL)
# matchups = getEventMatchups(eventInfo['link'])
# print(eventInfo)
# print(getEventMatchups('http://ufcstats.com/event-details/7c4ec656d8fcb867'))
# print(getEventMatchups(eventInfo['link']))

"""

url format 

ufcstats.com/statistics/fighters?char=a&page=8
                                 char=[a-z]&page=[1-9]+

for every letter 
    for every page
        visite every fighter page
        extract data 
        create fighter object
        add to database

""" 

def getFighterInfo(pageSoup,result):
    #for every row in the table body
    #get fighter first name,last name,w l d,height, weight,stance ,reach, nickname if exists
    rows = pageSoup.findAll('tr',class_='b-statistics__table-row')[2:]#exclude first 2 rows
    for row in rows:
        #11 column row 
        #first column is fighter first name
        #second column is fighter last name
        #third column is fighter nickname if exists
        #fourth column is fighter height
        #fifth column is fighter weight
        #sixth column is fighter reach
        #seventh column is fighter stance
        #eight column is fighter w
        #ninth column is fighter l
        #tenth column is fighter d
        #eleventh column is fighter belt status
        # print(row)
        cols = row.findAll('td')
        #ignore this fighter
        if re.findall(r'\d+',cols[4].text.strip()) == []:
            continue
        fighter_data = {}
        fighter_data['first_name'] = cols[0].a.text.strip()
        fighter_data['last_name'] = cols[1].a.text.strip()
        fighter_data['nickname'] = cols[2].text.strip()
        fighter_data['height'] = cols[3].text.strip()
        fighter_data['weight_class'] = cols[4].text.strip() #convert to int
        fighter_data['reach'] = cols[5].text.strip()
        fighter_data['stance'] = cols[6].text.strip()
        fighter_data['record'] = cols[7].text.strip() + '-' + cols[8].text.strip() + '-' + cols[9].text.strip()
        result.append(fighter_data)


def saveToFile(fighters):
    #fighters is a list of dictionaries append them to an existing file fighters.json
    #if the file doesn't exist create it
    if os.path.exists('fighters.json'):
        with open('fighters.json','r') as f:
            data = json.load(f)
            data.extend(fighters)
            with open('fighters.json','w') as f:
                json.dump(data,f)
    else:
        with open('fighters.json','w') as f:
            json.dump(fighters,f)

def scrapeFighters():
    fighterListUrlPrefix = "http://ufcstats.com/statistics/fighters?char="
    fighterListUrlSuffix = "&page="
    letters = "abcdefghijklmnopqrstuvwxyz"

    for char in letters:
        fighters = []
        currentUrl = fighterListUrlPrefix + char + fighterListUrlSuffix + "1"
        #visit page get max page number from table
        soup = BeautifulSoup(requests.get(currentUrl).content,"html.parser")
        maxPages = int(soup.findAll('li',class_='b-statistics__paginate-item')[-2].text.strip())
        getFighterInfo(soup,fighters)
        for i in range(1,maxPages + 1):
            if i == 1 :
                continue
            time.sleep(5)
            currentUrl = fighterListUrlPrefix + char + fighterListUrlSuffix + str(i)
            soup = BeautifulSoup(requests.get(currentUrl).content,"html.parser")
            getFighterInfo(soup,fighters)
        saveToFile(fighters)


def getFighterData(path):
    url = domain + path
    browser = webdriver.Chrome(options=options)
    # browser.implicitly_wait(10)
    browser.get(url)
    
    source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(source, 'html.parser')
    """
    
        fighter details structure
        ul 
            li <-- full name
            li <-- record
            li <-- nickname
            li
            li <-- age | date of birth
            li
            li <-- weightclass
            li
            li <-- height | reach
            li
            li <-- born location
            li 
            li 
            li 
            li
            li

    """
    ul = soup.select('.details ul.clearfix')[0]
    # print(ul)
    listItems = ul.findAll('li')
    nameSpaceIndex = listItems[0].span.text.find(' ')
    first_name = normalizeString(listItems[0].span.text[:nameSpaceIndex].strip())
    last_name = normalizeString(listItems[0].span.text[nameSpaceIndex + 1:].strip())
    fighter_data = {
        'first_name': first_name,
        'last_name': last_name,
        'record': listItems[1].span.text.split(' ')[0].strip(),
        'nick_name': normalizeString(listItems[2].span.text.strip()),
        'date_of_birth': datetime.strptime(listItems[4].findAll('span')[1].text.strip(),"%Y.%m.%d").date(),
        'weight_class': listItems[6].span.text.strip().upper().replace(" ","_"),
        'height': listItems[8].findAll('span')[0].text.strip(),
        'reach': listItems[8].findAll('span')[1].text.strip(),
    }

    return fighter_data


def normalizeString(string):
    return unicodedata.normalize('NFD',string).encode('ascii', 'ignore').decode("ascii").lower()