from fightEvaluator.scraper_funcs.fetchers import PlaywrightFetcher
from fightEvaluator.scraper_funcs.parsers import TapologyParser
import multiprocessing
import time

tapology_events_url = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"
DEFAULT_SCRAPE_DELAY = 15
def scrape_event(queue: multiprocessing.Queue,delay=DEFAULT_SCRAPE_DELAY):
    time.sleep(delay)
    fetcher = PlaywrightFetcher()
    parser = TapologyParser()

    fetch_results = fetcher.fetch(url=tapology_events_url)
    source = fetch_results['results']

    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_EVENT_LINK_DATA)
    fight_event_link = parse_results['link']
    fight_event_date = parse_results['date']

    fetch_results = fetcher.fetch(url=fight_event_link)
    source = fetch_results['results']

    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_MATCHUPS)

    queue.put( {
        'event':{'title':parse_results['title'],
                 'link':fight_event_link,   
                 'date':fight_event_date},
        'matchups':parse_results['matchups']
    })


def scrape_fighter_data(queue: multiprocessing.Queue,fighter_data_link,delay=DEFAULT_SCRAPE_DELAY):
    time.sleep(15)
    fetcher = PlaywrightFetcher()
    parser = TapologyParser()

    fetch_results = fetcher.fetch(url=fighter_data_link)
    source = fetch_results['results']
    
    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_FIGHTER_DATA)

    queue.put({fighter_data_link:parse_results})
