import re
import unicodedata
from pyquery import PyQuery as pq

domain = "https://www.tapology.com"

#normalize string to ascii from unicode
def normalizeString(string):
    return unicodedata.normalize('NFD',string).encode('ascii', 'ignore').decode("ascii").lower()


def extract_text(element):
    text = element.text()
    result = []
    if text:
        result.append(text)
    for child in element.children():
        result += extract_text(pq(child))
    
    return result

#grab fighter data from an element
def scrapeFighterData(element):
    atag = pq(element)('[class*="link-primary-red"]').eq(0)
    name = atag.text()
    link = atag.attr('href')

    return {'name':normalizeString(name),'link':domain + link}

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

        dataBoutWrapper = pq(li)("div[data-bout-wrapper]").children()[0]
        fighter_a,boutInfo,fighter_b = pq(dataBoutWrapper).children()
        
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


# for li in ulFightCard.find_all('li'):
    #     print(li)
    #     dataWrapper = li.div
    #     boutWrapper = dataWrapper.div
    #     # dataWrapperChildren = dataWrapper.contents#dataWrapper.find_all("div",recursive=False)
    #     # print(dataWrapper)
    #     # print(dataWrapperChildren)
    #     # if len(dataWrapperChildren) > 2:
    #     #     boutWrappper = dataWrapperChildren[1]#is second child
    #     fighterA,matchupInfo,fighterB = boutWrapper.find_all("div",recursive=False)
    #     matchupInfo = matchupInfo.div

    #     fighterA_a = fighterA.find('a')
    #     fighterB_a = fighterB.find('a')

    #     fighterAName = fighterA_a.text.strip()
    #     fighterBName = fighterB_a.text.strip()

    #     fighterALink = fighterA_a['href']
    #     fighterBLink = fighterB_a['href']

    #     eventType,weight_lbs,rounds = extract_text(matchupInfo)
    #     # print(fighterAName,fighterBName,eventType,weight_lbs,rounds)
         
    #     matchup = {
    #         'fighters_raw':[
    #         {
    #             'name':normalizeString(fighterAName),
    #             'link':domain + fighterALink
    #         },
    #         {
    #             'name':normalizeString(fighterBName),
    #             'link':domain + fighterBLink
    #         }
    #     ]}

    #     isprelim = False
    #     if re.match(r'Prelim',rounds):
    #         isprelim = True
    #     if eventType and "Prelim" in eventType:
    #         isprelim = True
             
    #     roundSearch = re.search(r'[0-9]+ x [0-9]+',rounds)
    #     if roundSearch:
    #         rounds = roundSearch.group(0)[0]
    #     else:
    #         continue #ignore this matchup
    #     matchup['weight_class'] = poundsToWeightClass(weight_lbs)
    #     matchup['rounds'] = rounds
    #     matchup['isprelim'] = isprelim
    #     matchups.append(matchup)