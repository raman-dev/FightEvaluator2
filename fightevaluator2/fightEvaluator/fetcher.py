#return string page source
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time

DRIVER_PATH='chromedriver-win64/chromedriver'
# DEFAULT_OPTIONS = Options()
# # options.add_argument("--headless=new")
# DEFAULT_OPTIONS.add_argument('--ignore-certificate-errors')
# DEFAULT_OPTIONS.add_argument('--ignore-ssl-errors')


# def getSourceRequests(url):
#     try:
#         response = requests.get(url)
#         page_source = response.text
#         print("PAGE RETRIEVED!")
#         return page_source
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")

#     return "fucked!"

class Fetcher:
    DEFAULT_OPTIONS = Options()
    # options.add_argument("--headless=new")
    DEFAULT_OPTIONS.add_argument('--ignore-certificate-errors')
    DEFAULT_OPTIONS.add_argument('--ignore-ssl-errors')
    def __init__(self):
        #initialize the selenium stuff here
        self.browser = None

    def __enter__(self):
        self.browser = webdriver.Chrome(options=Fetcher.DEFAULT_OPTIONS)
        return self

    def fetch(self,url,wait_time=0) -> str:
        

        self.browser.get(url)
        if wait_time > 0:
            time.sleep(wait_time)
        source = self.browser.page_source
        return source

    def __exit__(self,exception_type,exception_value,traceback):
        
        if exception_type:
            print(exception_type,exception_value)
        if traceback:
            print(traceback)

        self.browser.quit()
        self.browser = None
    
    #fetch using requests library
    @staticmethod
    def fetchWithRequests(url: str) -> str:
        try:
            response = requests.get(url)
            page_source = response.text
            # print("PAGE RETRIEVED!")
            return page_source
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        return "Something happened!"