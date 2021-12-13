import yaml
from concurrent.futures import ThreadPoolExecutor
from scrapers.washingtonpost import WashingtonPost
from scrapers.nytimes import NYTimes
from scrapers.apnews import APNews
from scrapers.foxnews import FoxNews
from scrapers.huffpost import HuffingtonPost
from utils.emailclient import CustomEmail

scrapers = [WashingtonPost, NYTimes, APNews, FoxNews, HuffingtonPost]

with open("config.yaml") as f:
    use_email = yaml.safe_load(f)['EMAIL']['USE_EMAIL']
    
def helper_func(params):
    global justchanged
    scraper, url = params
    processed = scraper.process_article(url)
    added=scraper.update_article(url, processed)
    if added:
        article, version_count = added
        justchanged.append((url, article, version_count))

if use_email:
    eclient = CustomEmail()

for s in scrapers:
    justchanged=[]
    current_scraper = s()
    urls = current_scraper.get_articles()
    pars = [(current_scraper, url) for url in urls]
    with ThreadPoolExecutor() as e:
        e.map(helper_func, pars)
    if justchanged and use_email:
        eclient.add_header(current_scraper.name)
        for url, article, version_count in justchanged:
            eclient.add_article(current_scraper.name, url, article, version_count)

if use_email and not eclient.empty:
    eclient.send()