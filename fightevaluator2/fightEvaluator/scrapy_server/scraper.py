from fetchers import PlaywrightFetcher
from parsers import TapologyParser

tapology_events_url = "https://www.tapology.com/search?term=ufc&search=Submit&mainSearchFilter=events"

def scrape_event():
    fetcher = PlaywrightFetcher()
    parser = TapologyParser()

    fetch_results = fetcher.fetch(url=tapology_events_url)
    parse_results = parser.parse(fetch_results['results'],TapologyParser.ParseType.PARSE_MATCHUPS)