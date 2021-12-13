import re
from scrapers.basescraper import BaseScraper


class APNews(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url_format = r"https://apnews.com/article/.+[a-z0-9]{32}"
        self.base_url = "https://apnews.com"
        self.starting_pages = ["https://apnews.com"]
        self.name = "apnews"
        self.url_exclusions = []
        self.headline_matches = [
            ("div", {"data-key": "card-headline"}),
            ("div", {"class": re.compile("headline-")}),
            ("h1", {"class":re.compile("headline-")})
        ]
        self.subhead_matches = []
        self.byline_matches = [
            ("span", {"class": re.compile("Component-bylines-")}, False),
            ("div", {"class": re.compile("byline-")}, False),
        ]
        self.content_matches = [
            ("div", {"class": "Article"}),
            ("article", {"class": re.compile("article-")}),
        ]
        self.content_exclusions = [
            ("div", {"class": re.compile("Component-hubPeekEmbed-")}),
            ("div", {"data-key": "feed-card-hub-peak"}),
            ("h1", {"class":re.compile("headline-")})
        ]
