from scrapers.washingtonpost import WashingtonPost
from scrapers.nytimes import NYTimes
from scrapers.apnews import APNews
from scrapers.foxnews import FoxNews
from scrapers.huffpost import HuffingtonPost
from concurrent.futures import ThreadPoolExecutor

scrapers = [WashingtonPost, NYTimes, APNews, FoxNews, HuffingtonPost]


def helperFunc(params):
    scraper, url = params
    processed = scraper.process_article(url)
    scraper.update_article(url, processed)


for s in scrapers:
    scraper = s()
    urls = scraper.get_articles()
    params = [(scraper, url) for url in urls]
    with ThreadPoolExecutor() as e:
        e.map(helperFunc, params)
