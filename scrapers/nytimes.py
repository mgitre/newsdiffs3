from scrapers.basescraper import BaseScraper


class NYTimes(BaseScraper):
    def __init__(self):
        self.url_format = (
            r"^https://(?:www\.)?nytimes\.com/\d{4}/\d{2}/\d{2}/[^.]+.html"
        )
        self.base_url = "https://www.nytimes.com"
        self.starting_pages = [
            "https://www.nytimes.com",
            "https://www.nytimes.com/section/todayspaper",
        ]
        self.name = "nytimes"
        self.url_exclusions = ["interactive"]
        self.headline_matches = [
            ("h1", {"itemprop": "headline"}),
            ("h1", {"data-testid": "headline"}),
            ("h1", {"class": "edye5kn2"}),
        ]
        self.subhead_matches = [
            ("p", {"id": "article-summary"}),
            ("p", {"class": "css-h99hf"}),
        ]
        self.byline_matches = [
            ("p", {"itemprop": "author"}),
            ("div", {"class": "css-vp77d3"}),
        ]
        self.content_matches = [
            ("section", {"itemprop": "articleBody"}),
            ("section", {"name": "articleBody"}),
        ]
