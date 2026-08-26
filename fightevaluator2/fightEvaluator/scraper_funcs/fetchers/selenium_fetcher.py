from .fetcher import Fetcher

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib3.exceptions import ReadTimeoutError
from selenium.webdriver.chrome.service import Service


import time
import random

class SeleniumFetcher(Fetcher):
    """
        NOTE
            USE CHROME FOR TESTING(SEPERATE EXECUTABLE/BINARY) TO USE FULL POWER OF SELENIUM
            NORMAL CHROME DOESN'T HAVE ALL CAPABILITIES AND REJECTS CUSTOM EXTENSIONS

            CANNOT USE ADBLOCK WITHOUT CHROME_FOR_TESTING
    """
    def __init__(self,path_to_binary,path_to_adblock=None,path_to_driver=None,options=None):
        self.path_to_driver = path_to_driver
        if path_to_binary is None:
            raise ValueError("MUST SPECIFY PATH TO CHROME_FOR_TESTING(not normal chrome) BINARY !!!")
        
        if options is None:
            # self.options.add_argument("--headless=new")            # modern headless mode
            self.options = Options()
            self.options.add_argument("--window-size=1920,1080")   # real desktop viewport
            
            self.options.binary_location = path_to_binary
            
            if not path_to_adblock is None:
                print(f"Adding extension at: \n\t: {path_to_adblock}")
                self.options.add_extension(path_to_adblock)
                self.options.add_argument("--enable-unsafe-extension-debugging")
                self.enable_webextensions=True
                # self.options.add_argument(f"--load-extension={path_to_adblock}")
                
            # self.options.page_load_strategy="none"
            self.options.add_argument("--no-sandbox")              # needed in many containers
            # self.options.add_argument("--disable-dev-shm-usage")   # avoid /dev/shm crashes in Docker
        self.driver = None

    def start(self):
        #logging need for debugging
        # service = Service(
        #     log_output="chromedriver.log",
        #     service_args=["--verbose"]
        # )

        self.driver = webdriver.Chrome(
            # service=service,
            options=self.options)
        
        print(f"Chrome started: {self.driver.service.service_url}")

    def stop(self):
        if self.driver is None:
            return
        
        print("Stopping Chrome...")
        self.driver.quit()  
        self.driver=None
    def __enter__(self):
        self.start()
        return self

    def __exit__(self,exec_type,exec_val,traceback):
        self.stop()


    def fetch(self,url) -> dict:
        print(f'selenium.fetching {url}')
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"driver.get ERROR: {type(e).__name__}: {e}")

            try:
                print(f"Driver details\n\tURL: {self.driver.current_url} \n\ttitle: {self.driver.title} \n\t isAlive: True")
                # print("Driver is still alive")
            except Exception as e2:
                print("DRIVER IS DEAD:", type(e2).__name__, e2)
                return Fetcher.get_result_dict(results=None,format=Fetcher.JSON,url=url)

        t_sleep = random.randrange(20,35)
        print(f'Selenium.fetcher sleeping for {t_sleep} seconds.')
        time.sleep(t_sleep)

        page_source = self.driver.page_source
        print(f'Retrieved page source.')
        return Fetcher.get_result_dict(results=page_source, 
                                       format=Fetcher.JSON, 
                                       url=url)
