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

def getUpcomingFightEvent(): #returns a dictionary of the next upcoming fight event
    fightEventData = {}
    return fightEventData