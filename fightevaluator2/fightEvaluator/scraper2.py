import re
import unicodedata
from pyquery import PyQuery as pq

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


def scrapeResults():#(source):
    d = pq(filename="test.html",encoding='utf-8')
    ul = d("#sectionFightCard > ul") #this returns pyquery object
    for li in ul("li"):
        #li is of type lxml.html.HtmlElement
        matchup = {}

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

        print(x)
        print(y)
        print()

        #non decision fromat is M:SS Round x of y
        #decision is full time
        # if "decision" in method: 
        # break
# scrapeResults()