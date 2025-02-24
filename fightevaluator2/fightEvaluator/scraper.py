import requests 
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import math
import re
# import unicodedata

from django.db.models import Q
from .models import WeightClass,Fighter,Assessment
from .forms import FightEventForm,FighterForm

EVENTS_URL = "http://ufcstats.com/statistics/events/completed"
#use tapology website its better and more comprehensive
EVENTS_URL2 = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
domain = "https://www.tapology.com"

DRIVER_PATH='chromedriver-win64/chromedriver'
options = Options()
# options.add_argument("--headless=new")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
import time

from .scraper2 import * 

# #normalize string to ascii from unicode
# def normalizeString(string):
#     return unicodedata.normalize('NFD',string).encode('ascii', 'ignore').decode("ascii").lower()


def getPageSource(url):
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    
    time.sleep(5)
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
        print(data_event_title,data_date)
        if data_date < today:
            break
        result['link'] = domain + data_link
        result['date'] = data_date
    # print(result)
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
            names = list(map(lambda x: x.lower(), name.split(' ')))
            name_index = "-".join(names)#search using this
            first_name = names[0]#try only first name
            last_name = names[-1]#last name may include middle name
            if len(name) > 1:
                last_name = " ".join(names[1:])

            print(first_name,last_name,name_index)

            first_name_and_last_name_contains=Q(first_name=first_name) & Q(last_name__contains=last_name)
            query_a = first_name_and_last_name_contains

            #first try 
            fighterObj = Fighter.objects.filter(name_index=name_index).first()
            if not fighterObj:            
                fighterObj = Fighter.objects.filter(query_a).first()

            if not fighterObj:
                #query fighter api for data
                fighterData = {}
                fighterObj = getFighterData(fighter['link'],fighterData)
                if fighterObj == None:
                    fighterData['data_api_link'] = fighter['link']
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

    # print('retrieved from => ',fightEventData['eventData']['link'])    
    soup = BeautifulSoup(source,'html.parser')#parse html
    # print the soup to a file
    # with open("output.html", "w", encoding="utf-8") as file:
    # # Writing the HTML content of the parsed soup to the file
    #     file.write(str(soup))
    # title = soup.find('div',class_='eventPageHeaderTitles').h1.text.strip()
    
    title = soup.find('h2').text.strip()
    fightEventData['eventData']['title'] = title

    """

        page structure 2024-03-25
            #sectionFightCard
                ul
                    li
                      data-bout-wrapper
                        div (another wrapper)
                            div -> fighter_a
                            div -> bout info container parent
                                div -> bout info container 
                            div -> fighter_b
    
    """
    #list of matchups
    matchups = scrapeMatchups(source) 
    for m in matchups:
        w = poundsToWeightClass(m['weight_class'])
        m['weight_class'] = w
    generateMatchupFighterObjs(matchups)
    fightEventData['matchups'] = matchups
    return fightEventData


#fetch and parse fighter detail page
def getFighterData(link,fighterData):
    source = getPageSource(link)
    soup = BeautifulSoup(source,'html.parser')
    
    fighterNameRecord = soup.find_all('div',class_='leading-tight')
    nameElement,recordElement = fighterNameRecord
    full_name = normalizeString(nameElement.text.strip())

    record = recordElement.text.strip().split('-')
    wins = int(record[0])
    losses = int(record[1])
    draws = int(record[2])
    
    names = list(map(lambda x: x.lower(),full_name.split(' ')))
    name_index = "-".join(names)
    print(full_name,name_index)
    
    potentialFighter = Fighter.objects.filter(name_index=name_index).first()
    if potentialFighter:
        return potentialFighter

    first_name = names[0]
    last_name = " ".join(names[1:])#full_name.split(' ')[-1]


    fighterData['first_name'] = first_name
    fighterData['last_name'] = last_name,
    fighterData['wins'] = wins,
    fighterData['losses'] = losses,
    fighterData['draws'] = draws
    
    fighterDetails = soup.find('div',id='standardDetails')
    scrapeFighterDetails(str(fighterDetails),fighterData)

    return None

TEST_LINK = "https://www.tapology.com/fightcenter/events/105840-ufc-297"
def getFightEventResults(link):
    source = getPageSource(link)
    #use link to get more info about event
    soup = BeautifulSoup(source,'html.parser')#parse html
    #list of matchups
    ulFightCard = soup.find('ul',class_='fightCard')
    outcomes = []
    for li in ulFightCard.findAll('li'):
        fightCardBout = li.div
        fightCardResultHolder = fightCardBout.find('div',class_='fightCardResultHolder')
        fightCardResult = fightCardResultHolder.find('div',class_='fightCardResult')
        time = fightCardResultHolder.find('span',class_='time').text.strip()
        method = fightCardResultHolder.find('span',class_='result').text.strip()
        
        outcomeData = {}
        outcomeData['time'] = time
        outcomeData['method'] = method
        
        for i,fightCardFighterBout in enumerate(fightCardBout.findAll('div',class_='fightCardFighterBout')):
            fighterName = fightCardFighterBout.find('div',class_='fightCardFighterName')
            name = normalizeString(fighterName.a.text.strip())
            outcomeData['fighter_'+str(i)] = name
            #check if class list contains win
            classes = fightCardFighterBout.get('class')
            if 'win' in classes:
                outcomeData['winner'] = 'fighter_'+str(i)
        outcomes.append(outcomeData)
    return outcomes

def getFightEventResults2(link):
    source = getPageSource(link)
    #use link to get more info about event
    matchupResults = scrapeResults(source)
    return matchupResults
#     print('valid fighteventForm')
# for every matchup find the fighter object in the database
# if fighter is not in database create fighter object

#read source from file fighter_details_test.html
# source = open('fighter_details_test.html','r').read()
# with open('fighter_details_test.html','r',encoding='utf-8') as f:
#     # source = f.read()
#     fighterDetails = BeautifulSoup(f,'html.parser')
#     print(getFighterDetails(fighterDetails,{}))

