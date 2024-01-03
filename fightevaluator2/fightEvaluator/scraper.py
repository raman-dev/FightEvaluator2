import requests 
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import math
import re
import unicodedata

from django.db.models import Q
from .models import WeightClass,Fighter,Assessment
from .forms import FightEventForm,FighterForm

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


def getPageSource(url):
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    
    source = browser.page_source
    browser.quit()
    return source

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
    
def generateMatchupFighterObjs(matchups):
    for matchup in matchups:
        for i,fighter in enumerate(matchup['fighters_raw']):
            #check if fighter is in database
            name = fighter['name']
            first_name = name.split(' ')[0]#try only first name
            last_name = name.split(' ')[-1]#last name may include middle name
            
            print(first_name,last_name)
            first_name_and_last_name_contains=Q(first_name=first_name) & Q(last_name__contains=last_name)
            query_a = first_name_and_last_name_contains
            
            fighterObj = Fighter.objects.filter(query_a).first()
            if not fighterObj:
                #query fighter api for data
                fighterData = getFighterData(fighter['link'])
                fighterForm = FighterForm(fighterData)#validate fighter data
                if fighterForm.is_valid():
                    #create fighter object
                    fighterObj = fighterForm.save()
                    
                    assessment = Assessment(fighter=fighterObj)
                    assessment.save()

                    fighterObj.assessment = assessment
                    print(fighterObj)
                else:
                    print(fighterForm.errors)
                    return
            if i == 0:
                matchup['fighter_a'] = fighterObj
            else:   
                matchup['fighter_b'] = fighterObj
    matchup.pop('fighters_raw')#no longer need this data
    # print(matchup)

def getUpcomingFightEvent(): #returns a dictionary of the next upcoming fight event
    fightEventData = {'eventData':{}}
    for k,v in extractLinkAndDate(EVENTS_URL2).items():
        fightEventData['eventData'][k] = v

    #use link to get more info about event
    source = getPageSource(fightEventData['eventData']['link'])
    
    soup = BeautifulSoup(source,'html.parser')#parse html
    title = soup.find('div',class_='eventPageHeaderTitles').h1.text.strip()
    fightEventData['eventData']['title'] = title

    #list of matchups
    ulFightCard = soup.find('ul',class_='fightCard')
    matchups = []
    for li in ulFightCard.findAll('li'):
        # print(li.div)
        fightCardBout = li.div
        matchup = {'fighters_raw':[]}

        for i,fightCardFighterBout in enumerate(fightCardBout.findAll('div',class_='fightCardFighterBout')):
            # print(fightCardFighterBout)
            fighterName = fightCardFighterBout.find('div',class_='fightCardFighterName')
            name = normalizeString(fighterName.a.text.strip())
            link = fighterName.a['href']
            matchup['fighters_raw'].append({'name':name,'link':domain+link})
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
    generateMatchupFighterObjs(matchups)
    fightEventData['matchups'] = matchups
    return fightEventData

def getFighterDetails(fighterDetailsSoup: BeautifulSoup,fighterData: dict) -> dict:
    for li in fighterDetailsSoup.findAll('li'):
        li_text = li.text.strip()
        if re.search(r'Height',li_text):
            #li item contains height
            #first span element contains height string
            height_string = li.span.text.strip()
            #3 height values if both feet'inch" and cm are present
            #1 height value if only cm is present
            height_match = re.findall(r'[0-9]+',height_string)#try feet'inch"
            height_inches = 0
            if len(height_match) == 1:
                height_inches = math.floor(int(height_match[0]) / 2.54)
            else:
                height_inches = int(height_match[0])*12 + int(height_match[1])
            fighterData['height'] = height_inches

        if re.search(r'Weight Class',li_text):
            #first span contains weight class
            weight_class = li.span.text.strip().replace(" ","_").upper()
            fighterData['weight_class'] = WeightClass[weight_class]

        if re.search(r'Reach',li_text):
            reach_string = li.find_all('span')[1].text.strip()
            reach_match = re.findall(r'[0-9]+',reach_string)
            reach_inches = 0
            if len(reach_match) == 2:
                reach_inches = int(reach_match[0])
            else:
                #if cm it is always gonna be the last match
                reach_inches = math.floor(int(reach_match[-1]) / 2.54)
            fighterData['reach'] = reach_inches

        if re.search(r'Date of Birth',li_text):
            dob_string = li.find_all('span')[-1].text.strip()#last span element
            dob = datetime.strptime(dob_string,"%Y.%m.%d").date()
            fighterData['date_of_birth'] = dob

def getFighterData(link):
    source = getPageSource(link)
    soup = BeautifulSoup(source,'html.parser')
    
    fighterNameHeader = soup.find('div',class_='fighterUpcomingHeader')
    record_h1,name_h1 = fighterNameHeader.find_all('h1')
    full_name = normalizeString(name_h1.text.strip())

    record = record_h1.text.strip().split('-')

    wins = int(record[0])
    losses = int(record[1])
    draws = int(record[2])
    
    first_name = full_name.split(' ')[0]
    last_name = full_name.split(' ')[-1]

    fighterData = {
        'first_name':first_name,
        'last_name':last_name,
        'wins': wins,
        'losses':losses,
        'draws':draws,
    }
    fighterDetailsUl = soup.find('div',id='stats').ul
    getFighterDetails(fighterDetailsUl,fighterData)

    return fighterData
#     print('valid fighteventForm')
# for every matchup find the fighter object in the database
# if fighter is not in database create fighter object

#read source from file fighter_details_test.html
# source = open('fighter_details_test.html','r').read()
# with open('fighter_details_test.html','r',encoding='utf-8') as f:
#     # source = f.read()
#     fighterDetails = BeautifulSoup(f,'html.parser')
#     print(getFighterDetails(fighterDetails,{}))

