from .fetcher import Fetcher
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

class PlaywrightFetcher(Fetcher):
    DEFAULT_TIMEOUT = 60000

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.current_page = None 
        self.initialized = False
        self.closed = False
    
    def start(self):
        if self.initialized == True:
            return
        playwright_ctx_manager = sync_playwright()
        self.playwright = playwright_ctx_manager.start()
        self.initialized = True

    def stop(self):
        if not self.initialized:
            return
        if not self.browser is None:
            print('\tClosing browser...')
            self.browser.close()
        self.playwright.stop()
        self.closed = True


    def fetch2(self,url):
        if self.closed :
            raise RuntimeError("Playwright Fetcher stopped/destroyed create new.")
        if not self.initialized:
            raise RuntimeError("Playwright Fetcher not initialized")
        
        if self.browser is None:
            self.browser = self.playwright.chromium.launch(headless=False)

        if self.current_page is None:
            self.current_page = self.browser.new_page()
        
        html_source = None
        try:
            self.current_page.goto(
                url=url,
                timeout=self.DEFAULT_TIMEOUT,
                wait_until="domcontentloaded")
            html_source = self.current_page.content()
        except TimeoutError as e:
            print(f'playwright.fetch2 timeout error for {url}')
            html_source = self.current_page.content()

        return Fetcher.get_result_dict(html_source, Fetcher.DICT, url)

    def fetch(self,url) -> dict:
        print(f'playwright.fetching {url}')

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            try:
                page.goto(
                    url=url,
                    timeout=self.DEFAULT_TIMEOUT,
                    wait_until="domcontentloaded")
                html_source = page.content()
            except TimeoutError as e:
                print(f'playwright.fetch2 timeout error for {url}')
                html_source = page.content()
            html_source = page.content()
            browser.close()

        return Fetcher.get_result_dict(html_source, Fetcher.DICT, url)