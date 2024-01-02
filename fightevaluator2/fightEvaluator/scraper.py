import requests 
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re
import unicodedata

from django.db.models import Q
from .models import WeightClass,Fighter
from .forms import FightEventForm

EVENTS_URL = "http://ufcstats.com/statistics/events/completed"
#use tapology website its better and more comprehensive
EVENTS_URL2 = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
domain = "https://www.tapology.com"

DRIVER_PATH='chromedriver-win64/chromedriver'
options = Options()
options.add_argument("--headless=new")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

#normalize string to ascii from unicode
def normalizeString(string):
    return unicodedata.normalize('NFD',string).encode('ascii', 'ignore').decode("ascii").lower()

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


def poundsToWeightClass(weight_lbs):
    weight_lbs = int(weight_lbs)
    if weight_lbs <= 110:
        return WeightClass['ATOMWEIGHT']
    elif weight_lbs <= 116:
        return WeightClass['STRAWWEIGHT']
    elif weight_lbs <= 126:
        return WeightClass['FLYWEIGHT']
    elif weight_lbs <= 136:
        return WeightClass['BANTAMWEIGHT']
    elif weight_lbs <= 146:
        return WeightClass['FEATHERWEIGHT']
    elif weight_lbs <= 156:
        return WeightClass['LIGHTWEIGHT']
    elif weight_lbs <= 171:
        return WeightClass['WELTERWEIGHT']
    elif weight_lbs <= 186:
        return WeightClass['MIDDLEWEIGHT']
    elif weight_lbs <= 206:
        return WeightClass['LIGHT_HEAVYWEIGHT']
    elif weight_lbs <= 266:
        return WeightClass['HEAVYWEIGHT']
    else:
        return WeightClass['CATCH_WEIGHT']
    
def getUpcomingFightEvent(): #returns a dictionary of the next upcoming fight event
    fightEventData = {'eventData':{}}
    for k,v in extractLinkAndDate(EVENTS_URL2).items():
        fightEventData['eventData'][k] = v

    #use link to get more info about event
    browser = webdriver.Chrome(options=options)
    browser.get(fightEventData['eventData']['link'])
    
    source = browser.page_source
    browser.quit()
    
    soup = BeautifulSoup(source,'html.parser')#parse html
    title = soup.find('div',class_='eventPageHeaderTitles').h1.text.strip()
    fightEventData['eventData']['title'] = title

    #list of matchups
    ulFightCard = soup.find('ul',class_='fightCard')
    matchups = []
    for li in ulFightCard.findAll('li'):
        # print(li.div)
        fightCardBout = li.div
        matchup = {'fighters':[]}

        for i,fightCardFighterBout in enumerate(fightCardBout.findAll('div',class_='fightCardFighterBout')):
            # print(fightCardFighterBout)
            fighterName = fightCardFighterBout.find('div',class_='fightCardFighterName')
            name = normalizeString(fighterName.a.text.strip())
            link = fighterName.a['href']
            matchup['fighters'].append({'name':name,'link':domain+link})
        weight_lbs = fightCardBout.find('span',class_='weight').text.strip()
        rounds = fightCardBout.find('td').text.strip()#
        
        isprelim = False
        if re.match(r'Prelim',rounds):
            isprelim = True
        
        roundSearch = re.search(r'[0-9]+ x [0-9]+',rounds)
        if roundSearch:
            rounds = roundSearch.group(0)[0]
        matchup['weight_class'] = poundsToWeightClass(weight_lbs)
        matchup['rounds'] = rounds
        matchup['isprelim'] = isprelim
        matchups.append(matchup)
    fightEventData['matchups'] = matchups
    return fightEventData

fightEventData = getUpcomingFightEvent()
# fightEventForm = FightEventForm(fightEventData['eventData'])
# if fightEventForm.is_valid():
    # print('valid fighteventForm')
#for every matchup find the fighter object in the database
# if fighter is not in database create fighter object
# for matchup in fightEventData['matchups']:
#     for fighter in matchup['fighters']:
#         #check if fighter is in database
#         name = fighter['name']
#         first_name = name.split(' ')[0]#try only first name
#         last_name = name.split(' ')[-1]#last name may include middle name
#         query = Q(first_name__equals=first_name) | Q(last_name__contains=last_name)
#         fighterObj = Fighter.objects.filter(query).first()
#         if not fighterObj:
#             #create fighter object
#             #query fighter api for data
        
