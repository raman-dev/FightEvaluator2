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
            # self.options.add_argument("--no-sandbox")              # needed in many containers
            # self.options.add_argument("--disable-dev-shm-usage")   # avoid /dev/shm crashes in Docker
        self.driver = None

    def start(self):
        self.driver = webdriver.Chrome(options=self.options)
        # print(self.driver.title)
        print(f"Chrome started: {self.driver.service.service_url}")

    def stop(self):
        if self.driver is None:
            return
        
        print("Stopping Chrome...")
        self.driver.quit()  

    def __enter__(self):
        self.start()
        return self

    def __exit__(self,exec_type,exec_val,traceback):
        self.stop()


    def fetch(self,url) -> dict:
        print(f'selenium.fetching {url}')
        # try:
        #     self.driver.get(url)
        # except Exception as e:
        #     print(f"Timeout loading {url}: {e}")
        page_source = None
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"driver.get ERROR: {type(e).__name__}: {e}")

            try:
                print("Driver current URL:", self.driver.current_url)
                print("Driver title:", self.driver.title)
                print("Driver is still alive")
            except Exception as e2:
                print("DRIVER IS DEAD:", type(e2).__name__, e2)
                return Fetcher.get_result_dict(results=None,format=Fetcher.JSON,url=url)

        t_sleep = random.randrange(20,35)
        print(f'Selenium.fetcher sleeping for {t_sleep} seconds.')
        time.sleep(t_sleep)
        page_source = self.driver.page_source
        
        return Fetcher.get_result_dict(results=page_source, 
                                       format=Fetcher.JSON, 
                                       url=url)
