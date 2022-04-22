from scrapers.basescraper import BaseScraper


class WashingtonPost(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url_format = r"https://www\.washingtonpost\.com/(?:politics|nation|world|elections|us-policy|business|entertainment|travel|advice|obituaries|technology|education)/(?:[^/]*/)?(?:[^/]*/)?\d{4}/\d{2}/\d{2}/(?:[^/]*/|[^.]*.html)"
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
            ("span", {"data-sc-c":"author"}, False),
            ("div", {"data-qa":"author-byline"}, False),
            ("div", {"class": "author-names"}, False),
            ("div", {"class": "contributor"}, False),
            ("a", {"data-qa": "author-name"}, False),
        ]
        self.content_matches = [
            ("article", {"data-qa": "main"}),
            ("div", {"class": "article-body"}),
            ("div", {"class": "main"}),
        ]
        self.content_exclusions = [
            ("a",{"data-qa": "intersitial-link"}),
            ("figure",{}),
            ("div", {"data-qa": "article-body-ad"}),
            ("div", {"class": "hide-for-print"}),
        ]