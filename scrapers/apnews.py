from scrapers.basescraper import BaseScraper
import re


class APNews(BaseScraper):
    def __init__(self):
        # self.url_format = r"https://www\.washingtonpost\.com/(?:politics|nation|world|elections|us-policy)/(?:[^/]*/)?(?:[^/]*/)?\d{4}/\d{2}/\d{2}/(?:[^/]*/|[^.]*.html)"
        self.url_format = r"https://apnews.com/article/.+[a-z0-9]{32}"
        self.base_url = "https://apnews.com"
        self.starting_pages = ["https://apnews.com"]
        self.name = "apnews"
        self.url_exclusions = []
        self.headline_matches = [
            ("div", {"data-key": "card-headline"}),
            ("div", {"class": re.compile("headline-")}),
        ]
        self.subhead_matches = []
        self.byline_matches = [
            ("span", {"class": re.compile("Component-bylines-")}),
            ("div", {"class": re.compile("byline-")}),
        ]
        self.content_matches = [
            ("div", {"class": "Article"}),
            ("article", {"class": re.compile("article-")}),
        ]
