
from datetime import datetime
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import unicodedata
import re
from rich import print as rprint

domain = "https://www.tapology.com"

def normalizeString(string):
    return (
        unicodedata.normalize("NFD", string)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )


def scrapeFighterNameAndLink(element, result_only=False):
    fighterPQ = pq(element)

    atag = fighterPQ('[class*="link-primary-red"]').eq(0)
    name = normalizeString(atag.text())

    if result_only == True:
        isWinner = False
        for span in fighterPQ("span"):
            if "Up to" in pq(span).text():
                isWinner = True
                break
        return {"name": name, "isWinner": isWinner}

    link = atag.attr("href")
    return {"name": name, "link": domain + link}


def scrapeWeightlbs(s: str):
    # grab a 3 digit number from string
    weightPattern = re.compile("(1|2)[0-9][0-9]")
    match = weightPattern.search(s)
    if match:
        return int(match.group(0))
    return None


def scrapePrelimStatus(s: str):
    isPrelimPattern = re.compile("Prelim")
    if isPrelimPattern.search(s):
        return True
    return False


def scrapeRounds(s: str):
    roundsPattern = re.compile("(3|5) x 5")
    match = roundsPattern.search(s)
    if not match:
        return None
    return int(match.group(0).split()[0])


def scrapeMatchups(source):
    # Writing the HTML content of the parsed soup to the file
    d = pq(source)  # filename="test_0.html")
    # d -> $ in jquery
    ul = d("#sectionFightCard > ul")  # this returns pyquery object
    
    matchups = []
    for li in ul("li"):
        # li is of type lxml.html.HtmlElement
        matchup = {}

        # dataBoutWrapper = pq(li)("div[data-bout-wrapper]").children()[0]
        dataBoutWrapper = pq(li)("div[data-bout-wrapper]:first")
        children = pq(dataBoutWrapper).children()

        rprint(f"num children =>  {len(children)}")
    
        
        parentIndex = len(children) - 2  # second last child
        dataParent = children[parentIndex]
        fighter_a, boutInfo, fighter_b = pq(dataParent).children()

        x = scrapeFighterNameAndLink(fighter_a)
        y = scrapeFighterNameAndLink(fighter_b)
        matchup["fighters_raw"] = [x, y]
        m = pq(boutInfo).text()
        # if contains 5 x 5 -> 5 rounder
        # if contains Prelim -> on prelims else on main card
        # check for an int that is valid 115,125,135,145,155,170,185,205,265
        isRumoured = re.compile("Prelim|Main Card|Co-Main|Main Event")
        if not isRumoured.search(m):
            # not a valid matchup # print(m)
            continue
        # grab prelimStatus
        isPrelim = scrapePrelimStatus(m)
        # grab the weightclass
        weightlbs = scrapeWeightlbs(m)
        # grab rounds
        rounds = scrapeRounds(m)
        if not weightlbs or not rounds:  # not a valid matchup
            continue
        matchup["weight_class"] = weightlbs
        matchup["rounds"] = rounds
        matchup["isprelim"] = isPrelim
        rprint(matchup)
        matchups.append(matchup)

    return matchups
def eventLinkParse(source: str):
    soup = BeautifulSoup(source, 'html.parser')
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
        # print(data_event_title,data_date)
        if data_date < today:
            break
        result['link'] = domain + data_link
        result['date'] = str(data_date)
    # print(result)
    return result

if __name__ == "__main__":
    with open("input.html",encoding="utf-8") as file:
        source = ""
        for line in file.readlines():
            source += line
        result = scrapeMatchups(source)
        print(result)

