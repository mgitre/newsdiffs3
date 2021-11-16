from concurrent.futures import ThreadPoolExecutor
from scrapers.washingtonpost import WashingtonPost
from scrapers.nytimes import NYTimes
from scrapers.apnews import APNews
from scrapers.foxnews import FoxNews
from scrapers.huffpost import HuffingtonPost

scrapers = [WashingtonPost, NYTimes, APNews, FoxNews, HuffingtonPost]


def helper_func(params):
    scraper, url = params
    processed = scraper.process_article(url)
    scraper.update_article(url, processed)


for s in scrapers:
    current_scraper = s()
    urls = current_scraper.get_articles()
    pars = [(current_scraper, url) for url in urls]
    with ThreadPoolExecutor() as e:
        e.map(helper_func, pars)
