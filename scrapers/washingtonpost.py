from scrapers.basescraper import BaseScraper


class WashingtonPost(BaseScraper):
    def __init__(self):
        self.url_format = r"https://www\.washingtonpost\.com/(?:politics|nation|world|elections|us-policy)/(?:[^/]*/)?(?:[^/]*/)?\d{4}/\d{2}/\d{2}/(?:[^/]*/|[^.]*.html)"
        self.base_url = "https://washingtonpost.com"
        self.starting_pages = ["https://washingtonpost.com"]
        self.name = "washingtonpost"
        self.url_exclusions = ["live-updates"]
        self.headline_matches = [
            ("h1", {"data-qa": "headline"}),
            ("h1", {"class": "title"}),
            ("h1", {"itemprop": "headline"}),
        ]
        self.subhead_matches = [
            ("h2", {"data-pb-field": "subheadlines.basic"}),
            ("h2", {"data-qa": "subheadline"}),
        ]
        self.byline_matches = [
            ("div", {"class": "author-names"}),
            ("div", {"class": "contributor"}),
            ("a", {"data-qa": "author-name"}),
        ]
        self.content_matches = [
            ("div", {"class": "article-body"}),
            ("article", {"data-qa": "main"}),
            ("div", {"class": "main"}),
        ]
