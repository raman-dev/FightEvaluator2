import re
import unicodedata
from pyquery import PyQuery as pq
from .models import WeightClass
import math
from datetime import datetime

domain = "https://www.tapology.com"

#normalize string to ascii from unicode
def normalizeString(string):
    return unicodedata.normalize('NFD',string).encode('ascii', 'ignore').decode("ascii").lower()


def extract_text(element: pq):
    text = element.text()
    result = []
    if text:
        result.append(text)
    for child in element.children():
        result += extract_text(pq(child))
    
    return result

def scrapeFighterDetails(fighterDetailsDiv,fighterData) -> dict:
    data = []
    result = pq(fighterDetailsDiv)("span")
    n = len(result)
    for i in range(0,n - 1):
        data.append(pq(result[i]).text())
    """
   0 'Gabriel Miranda' : name 
   1 'Fly' : nickname
   2 '17-6-0 (Win-Loss-Draw)' : record
   3 '1 Win': streak
   4 '34'   : age
   5 '1990 Mar 25': date-of-birth
   6 '5\'11" (180cm)' : height
   7 '71.0" (180cm)': reach
   8 'Featherweight' : weightclass
   9 '145.0 lbs': last weigh-in
     'Astra Fight Team'
     'September 09, 2023 in UFC'
     '$0 USD'
     'Telêmaco Borba, Paraná, Brazil' 
     
     2025-08-10 new query result structure
     0 name
     1 nickname
     2 record
     3 streak
     4 
    
     
    """
    height_pattern = re.compile(r"(\d)'(\d{1,2})\"\s+\(\d{3}cm\)")
    dob_pattern = re.compile(r"(\d{4})\s+(\w{3})\s+(\d{1,2})")
    reach_pattern = re.compile(r"((\d{2}\.\d+)|(\d{2}))\"\s+\(\d{3}cm\)")

    print(data)
    # height_string = data[6]
    #3 height values if both feet'inch" and cm are present
    #1 height value if only cm is present
    fighterData['height'] = 0
    fighterData['reach'] = 0
    fighterData['date_of_birth'] = 'N/A'
    fighterData['weight_class'] = WeightClass.LIGHTWEIGHT
    for d in data:
        weight_class = d.replace(" ","_").lower()
        height_match = re.search(height_pattern,d)#try feet'inch"
        reach_match = re.search(reach_pattern,d)
        dob_match = re.search(dob_pattern,d)
        # height_inches = 0
        # if len(height_match) == 1:
        #     height_inches = math.floor(int(height_match[0]) / 2.54)
        # if len(height_match) > 1:
        #     height_inches = int(height_match[0])*12 + int(height_match[1])
        if height_match:
            feet, inches = map(int, height_match.groups())
            height_inches = feet * 12 + inches
            fighterData['height'] = height_inches
        elif reach_match:
            reach_val = float(reach_match.group(1))
            reach_inches = int(round(reach_val))
            fighterData['reach'] = reach_inches
        elif weight_class != 'n/a' and  weight_class in WeightClass:
            fighterData['weight_class'] = WeightClass[weight_class.upper()]#first lower to query then upper to reference wtf
        elif dob_match:
            print('dob_string', d)
            dob = datetime.strptime(d, "%Y %b %d").date()
            fighterData['date_of_birth'] = dob

    #search all items of list since sometimes the list is in wrong order
    # reach_string = data[7].strip()
    # reach_match = re.findall(r'[0-9]+',reach_string)
    # reach_inches = 0
    # if len(reach_match) == 2:
    #     reach_inches = int(reach_match[0])
    # else:
    #     #if cm it is always gonna be the last match
    #     if reach_match != []:
    #         reach_inches = math.floor(int(reach_match[-1]) / 2.54)
    # fighterData['reach'] = reach_inches
    # dob_string = data[5].strip()#last span element
    # if dob_string != 'N/A':
    #     print('dob_string',dob_string)
    #     dob = datetime.strptime(dob_string,"%Y %b %d").date()
    #     fighterData['date_of_birth'] = dob
    # else:
    #     fighterData['date_of_birth'] = 'N/A'
    # print(data)

#grab fighter data from an element
def scrapeFighterData(element,result_only=False):
    fighterPQ = pq(element)
    
    atag = fighterPQ('[class*="link-primary-red"]').eq(0)
    name = normalizeString(atag.text())
    
    if result_only == True:
        isWinner = False
        for span in fighterPQ("span"):
            if "Up to" in pq(span).text():
                isWinner = True
                break
        return {'name':name,'isWinner':isWinner}
    
    link = atag.attr('href')
    return {'name':name,'link':domain + link}

def scrapeWeightlbs(s: str):
    #grab a 3 digit number from string
    weightPattern = re.compile('(1|2)[0-9][0-9]')
    match = weightPattern.search(s)
    if match:
        return int(match.group(0))
    return None

def scrapePrelimStatus(s: str):
    isPrelimPattern = re.compile('Prelim')
    if isPrelimPattern.search(s):
        return True
    return False

def scrapeRounds(s: str):
    roundsPattern = re.compile('(3|5) x 5')
    match = roundsPattern.search(s)
    if not match:
        return None
    return int(match.group(0).split()[0])

def scrapeMatchups(source):
    # Writing the HTML content of the parsed soup to the file
    d = pq(source)#filename="test_0.html")
    #d -> $ in jquery
    ul = d("#sectionFightCard > ul") #this returns pyquery object
    matchups = []
    for li in ul("li"):
        #li is of type lxml.html.HtmlElement
        matchup = {}

        # dataBoutWrapper = pq(li)("div[data-bout-wrapper]").children()[0]
        dataBoutWrapper = pq(li)("div[data-bout-wrapper]:first")
        children = pq(dataBoutWrapper).children()
        # print(pq(children))
        
        dataParent = children[0]
        if len(children) == 3:
            dataParent = children[1]

        fighter_a,boutInfo,fighter_b = pq(dataParent).children()
        
        x = scrapeFighterData(fighter_a)
        y = scrapeFighterData(fighter_b)
        matchup['fighters_raw'] = [x,y]
        m = pq(boutInfo).text()
        #if contains 5 x 5 -> 5 rounder
        #if contains Prelim -> on prelims else on main card
        #check for an int that is valid 115,125,135,145,155,170,185,205,265
        isRumoured = re.compile('Prelim|Main Card|Co-Main|Main Event')
        if not isRumoured.search(m):
            #not a valid matchup # print(m)
            continue
        #grab prelimStatus
        isPrelim = scrapePrelimStatus(m)
        #grab the weightclass
        weightlbs = scrapeWeightlbs(m)
        #grab rounds
        rounds = scrapeRounds(m)
        if not weightlbs or not rounds:#not a valid matchup
            continue
        matchup['weight_class'] = weightlbs
        matchup['rounds'] = rounds
        matchup['isprelim'] = isPrelim
        matchups.append(matchup) 
        
    return matchups


def scrapeResults(source):
    # d = pq(filename="results_test.html",encoding='utf-8')
    d = pq(source)
    ul = d("#sectionFightCard > ul") #this returns pyquery object
    matchupResults = []
    for i,li in enumerate(ul("li")):
        #li is of type lxml.html.HtmlElement
        # dataBoutWrapper = pq(li)("div[data-bout-wrapper]").children()[0]
        dataBoutWrapper = pq(li)("div[data-bout-wrapper]:first")
        children = pq(dataBoutWrapper).children()
        # print(pq(children))
        methodDataParent,resultDataParent,_ = children
        methods = []
        for span in pq(methodDataParent)("span"):
            methods.append(pq(span).text())
        
        _,method,roundTimes = methods
        fighter_a,_,fighter_b = pq(resultDataParent).children()
        
        x = scrapeFighterData(fighter_a,result_only=True)
        y = scrapeFighterData(fighter_b,result_only=True)

        result = {
            'fighters':[x,y]
        }
        
        #non decision fromat is M:SS Round x of y
        #decision is full time
        method = method.split(",")[0].lower()
        if 'decision' in method: 
            result['method'] = 'decision'
        elif 'ko/tko' in method:
            result['method'] = 'ko'
        elif 'submission' in method:
            result['method'] = 'submission'
        elif 'draw' in method:
            result['method'] = 'draw'
        else:
            result['method'] = 'no contest'
        
        # print(roundTimes,result['method'],method)
        if result['method'] == 'decision' or result['method'] == 'draw':
            #rounds = 3 or 5
            #time  = 15:00 or 25:00
            if "15:00" in roundTimes:
                result['final_round'] = '3'
            else:
                result['final_round'] = '5'#last round of fight
            result['time'] = '5:00' #final round time
        else:
            #format is Round X of Y
            #M:SS Round X of Y
            timeMatch = re.search(r'[0-5]\:[0-5][0-9]',roundTimes)
            roundMatch = re.search(r'Round [1-5] of [1-5]',roundTimes)
            result['time'] = timeMatch.group(0)
            result['final_round'] = re.search(r'[1-5]',roundMatch.group(0)).group(0)
        # print(result)
        matchupResults.append(result)
    return matchupResults