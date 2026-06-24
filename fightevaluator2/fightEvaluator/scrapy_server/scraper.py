from fetchers import PlaywrightFetcher
from parsers import TapologyParser

tapology_events_url = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"

def scrape_event():
    fetcher = PlaywrightFetcher()
    parser = TapologyParser()

    fetch_results = fetcher.fetch(url=tapology_events_url)
    source = fetch_results['results']

    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_EVENT_LINK_DATA)
    fight_event_link = parse_results['link']
    fight_event_date = parse_results['event']

    fetch_results = fetcher.fetch(url=fight_event_link)
    source = fetch_results['results']

    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_MATCHUPS)

    return {
        'event':{'title':parse_results['title'],
                 'link':fight_event_link,   
                 'date':fight_event_date},
        'matchups':parse_results['matchups']
    }


def scrape_fighter_data(fighter_data_link):
    fetcher = PlaywrightFetcher()
    parser = TapologyParser()

    fetch_results = fetcher.fetch(url=fighter_data_link)
    source = fetch_results['results']
    
    parse_results = parser.parse(source,TapologyParser.ParseType.PARSE_FIGHTER_DATA)

    return {fighter_data_link:parse_results}
