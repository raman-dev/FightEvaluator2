from bs4 import BeautifulSoup
import requests

url = 'https://www.tapology.com/fightcenter/events/101866-ufc-fight-night'#'http://ufcstats.com/statistics/events/completed'

page = requests.get(url)

# print(page.text)
soup = BeautifulSoup(page.content,"html.parser")
# findResult = soup.find('tr',class_="b-statistics__table-row_type_first")
print(soup)



