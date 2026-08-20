from .fetcher import Fetcher

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib3.exceptions import ReadTimeoutError


import time
import random

class SeleniumFetcher(Fetcher):
    
    def __init__(self,options=None):
        if options is None:
            # self.options.add_argument("--headless=new")            # modern headless mode
            self.options = Options()
            self.options.add_argument("--window-size=1920,1080")   # real desktop viewport
            self.options.add_argument("--no-sandbox")              # needed in many containers
            self.options.add_argument("--disable-dev-shm-usage")   # avoid /dev/shm crashes in Docker
        self.driver = None

    def start(self):
        self.driver = webdriver.Chrome(options=self.options)
        print(self.driver.title)

    def stop(self):
        if self.driver is None:
            return
        self.driver.quit()

    def __enter__(self):
        self.start()

    def __exit__(self):
        self.stop()


    def fetch(self,url) -> dict:
        print(f'selenium.fetching {url}')
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Timeout loading {url}: {e}")
        time.sleep(random.randrange(50,65))
        return Fetcher.get_result_dict(results=self.driver.page_source, 
                                       format=Fetcher.JSON, 
                                       url=url)
