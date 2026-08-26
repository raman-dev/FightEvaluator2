from fightEvaluator.scraper_funcs.fetchers import PlaywrightFetcher,SeleniumFetcher
from fightEvaluator.scraper_funcs.parsers import TapologyParser
import multiprocessing
import time
import os


# fetcher = PlaywrightFetcher()
# fetcher = SeleniumFetcher(path_to_adblock=path_to_adblock) cannot use global loses connection with webdriver

def delay(func):
    def wrapper(*args,**kwargs):
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # print(f'Current path: \n\t{current_dir}')
        time.sleep(15)
        func(*args,**kwargs)
    return wrapper

tapology_events_url = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
DEFAULT_SCRAPE_DELAY = 15

script_path = os.path.dirname(os.path.abspath(__file__)) 
path_to_adblock= script_path + "\\adblock-crx\\chromium.crx"
# path_to_adblock = script_path + "\\adblock-crx\\ublock_crx_extract"
path_to_binary = script_path + "\\chrome-win64\\chrome.exe"#
path_to_driver = script_path + "\\chromedriver-win64\\chromedriver.exe"
@delay
def scrape_event(queue: multiprocessing.Queue,delay=DEFAULT_SCRAPE_DELAY,link=None,date=None):
    # time.sleep(delay)

    parser = TapologyParser()
    with SeleniumFetcher(path_to_binary=path_to_binary,
                         path_to_driver=path_to_driver,
                         path_to_adblock=path_to_adblock) as fetcher:
        
        if link is None:
            fetch_results = fetcher.fetch(url=tapology_events_url)
            source = fetch_results['results']

            parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_EVENT_LINK_DATA)
            fight_event_link = parse_results['link']
            fight_event_date = parse_results['date']
        else:
            fight_event_link = link
            fight_event_date = date

        fetch_results = fetcher.fetch(url=fight_event_link)

    source = fetch_results['results']

    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_MATCHUPS)

    queue.put( {
        'event':{'title':parse_results['title'],
                 'link':fight_event_link,   
                 'date':fight_event_date},
        'matchups':parse_results['matchups']
    })

@delay
def scrape_fighter_data(queue: multiprocessing.Queue,fighter_data_link,delay=DEFAULT_SCRAPE_DELAY):
    # time.sleep(delay)

    with SeleniumFetcher(path_to_binary=path_to_binary,
                         path_to_driver=path_to_driver,
                         path_to_adblock=path_to_adblock) as fetcher:
        fetch_results = fetcher.fetch(url=fighter_data_link)

    source = fetch_results['results']

    parser = TapologyParser()
    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_FIGHTER_DATA)

    queue.put({fighter_data_link:parse_results})

@delay
def scrape_fight_event_results(queue: multiprocessing.Queue,fight_event_results_link,delay=DEFAULT_SCRAPE_DELAY):
    # time.sleep(delay)

    with SeleniumFetcher(path_to_binary=path_to_binary,
                         path_to_driver=path_to_driver,
                         path_to_adblock=path_to_adblock) as fetcher:
        fetch_results = fetcher.fetch(url=fight_event_results_link)

    source = fetch_results['results']
    
    parser = TapologyParser()
    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_FIGHT_EVENT_RESULTS)

    queue.put({fight_event_results_link:parse_results})
