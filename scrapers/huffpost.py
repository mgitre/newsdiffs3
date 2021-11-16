from scrapers.basescraper import BaseScraper


class HuffingtonPost(BaseScraper):
    def __init__(self):
        super().__init__()
        self.url_format = r"https://(?:www\.)?huffpost\.com/entry/.+[a-z0-9]{24}"
        self.base_url = "https://huffpost.com"
        self.starting_pages = ["https://huffpost.com"]
        self.name = "huffpost"
        self.url_exclusions = []
        self.headline_matches = [("h1", {"class": "headline"})]
        self.subhead_matches = [("div", {"class": "dek"})]
        self.byline_matches = [("div", {"class": "author-list"}, False)]
        self.content_matches = [
            ("section", {"id": "entry-body"}),
        ]
