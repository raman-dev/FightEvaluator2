import requests 
from bs4 import BeautifulSoup
from datetime import datetime
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
        data_event_title = data[0].a.text.strip()
        #skip non fight nights and non ppvs
        if re.search(r'(UFC\s+([0-9]+))|UFC\s+Fight\s+Night',data_event_title) == None:
            # print(data_event_title,'not a ufc event')
            continue
        data_link = data[0].a['href']
        #get date from data object
        data_date = datetime.strptime(data[2].text.strip(),"%Y.%m.%d").date()
        #compare today and date when the distance from today and date increases break loop
        if data_date < today:
            break
        result['link'] = domain + data_link
        result['date'] = data_date
    return result

def getUpcomingFightEvent(): #returns a dictionary of the next upcoming fight event
    fightEventData = {}
    for k,v in extractLinkAndDate(EVENTS_URL2).items():
        fightEventData[k] = v

    #use link to get more info about event
    browser = webdriver.Chrome(options=options)
    browser.get(fightEventData['link'])
    
    source = browser.page_source
    browser.quit()
    
    soup = BeautifulSoup(source,'html.parser')#parse html
    title = soup.find('div',class_='eventPageHeaderTitles').h1.text.strip()
    fightEventData['title'] = title

    #list of matchups
    ulFightCard = soup.find('ul',class_='fightCard')
    matchups = []
    for li in ulFightCard.findAll('li'):
        # print(li.div)
        fightCardBout = li.div
        matchup = {}
        for i,fightCardFighterBout in enumerate(fightCardBout.findAll('div',class_='fightCardFighterBout')):
            # print(fightCardFighterBout)
            fighterName = fightCardFighterBout.find('div',class_='fightCardFighterName')
            name = fighterName.a.text.strip()
            link = fighterName.a['href']
            matchup['fighter_'+str(i+1)] = {'name':name,'link':domain+link}
        matchups.append(matchup)
    
    
    return fightEventData

getUpcomingFightEvent()