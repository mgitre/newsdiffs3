from scrapers.basescraper import BaseScraper


class FoxNews(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url_format = r"^https://(?:www\.)?foxnews\.com/(?:media|entertainment|politics|us|science|sports|opinion|lifestyle|health|tech)/.+"
        self.base_url = "https://www.foxnews.com"
        self.starting_pages = ["https://www.foxnews.com"]
        self.name = "foxnews"
        self.url_exclusions = ["cartoons-slideshow"]
        self.headline_matches = [("h1", {"class": "headline"})]
        self.subhead_matches = [("h2", {"class": "sub-headline"})]
        self.byline_matches = [("div", {"class": "author-byline"}, False)]
        self.content_matches = [("div", {"class": "article-body"})]
