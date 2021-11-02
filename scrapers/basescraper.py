import re
import datetime
from utils.request_utils import getHTML
from utils.database_utils import get_article_urls_within_time, get_database, get_article
from models.article import ArticleVersion
from bs4 import BeautifulSoup


class BaseScraper:
    def __init__(self):
        pass

    def get_articles_from_pages(self, pages):
        articles = []
        for starting_page in pages:
            # gets a soup object for the initial page
            homepage_soup = BeautifulSoup(getHTML(starting_page), features="lxml")
            a_tags = homepage_soup.find_all("a", href=True)
            # iterates over any hyperlink that has an href
            for tag in a_tags:
                # fixes annoying slash stuff and query urls
                href = tag["href"]
                if not href:
                    continue
                if href[:2] == "//":
                    href = "https" + href
                elif href[0] == "/":
                    href = self.base_url + href
                href = href.split("?")[0]

                # continues if not a valid url
                valid = re.search(self.url_format, href)
                if valid is None:
                    continue

                # formats the url
                url = valid.group(0)
                url = self.format_url(url)

                # checks to see if url matches any of the exclusion strings
                if any(exclusion in url for exclusion in self.url_exclusions):
                    continue

                # checks if already been added
                if url in articles:
                    continue

                # if passed all checks, append to articles
                articles.append(url)
        return articles

    # loads articles from database that were last modified within (default: 7) days
    def get_articles_from_database(self):
        collection = get_database()[self.name]
        articles = get_article_urls_within_time(collection)
        return articles

    # gets articles from scraping and from database, and merges them.
    def get_articles(self):
        from_pages = self.get_articles_from_pages(self.starting_pages)
        from_database = self.get_articles_from_database()
        articles = from_pages + list(set(from_database) - set(from_pages))
        return articles

    # updates url of database entry
    def update_url(self, old_url, new_url):
        collection = get_database()[self.name]
        collection.update_one({"url": old_url}, {"$set": {"url": new_url}})

    def process_article(self, url):
        try:
            old_url = url
            html, url = getHTML(url, return_updated_url=True)
            if url != old_url:
                self.update_url(old_url, url)
            soup = BeautifulSoup(html, features="lxml")

            headline = None
            for name, attrs in self.headline_matches:
                match_attempt = soup.find(name, attrs)
                if match_attempt:
                    headline = match_attempt.get_text()
                    break

            subhead = None
            for name, attrs in self.subhead_matches:
                match_attempt = soup.find(name, attrs)
                if match_attempt:
                    subhead = match_attempt.get_text()
                    break

            byline = None
            for name, attrs in self.byline_matches:
                matchAttempt = soup.find(name, attrs)
                if matchAttempt:
                    bylinesoup = matchAttempt
                    # fix to get rid of annoying extra text
                    for hidden in bylinesoup.find_all(attrs={"class": "hidden"}):
                        hidden.decompose()
                    # this is ugly but so are a lot of bylines, so....
                    byline = re.sub(
                        r"\s+", " ", bylinesoup.get_text().replace(u"\xa0", " ").strip()
                    )
                    break

            content = None
            for name, attrs in self.content_matches:
                articlebody = soup.find(name, attrs)
                if articlebody:
                    paragraphs = []
                    for paragraph in articlebody.find_all(
                        ["p", "h1", "h2", "h3", "h4", "h5", "h6"]
                    ):
                        text = paragraph.get_text()
                        if text == text.upper():
                            continue
                        if text == "Read more:":
                            break
                        else:
                            paragraphs.append(
                                "<{0}>{1}</{0}>".format(paragraph.name, text)
                            )
                    content = "\n".join(paragraphs)
                    break

            return ArticleVersion(
                {
                    "headline": headline,
                    "subhead": subhead,
                    "byline": byline,
                    "content": content,
                }
            )
        except Exception as e:
            print(e)

    def update_article(self, url, version):
        try:
            collection = get_database()[self.name]
            stored_article = get_article(collection, url)
            if not stored_article:
                collection.insert(
                    {
                        "url": url,
                        "last_modified": datetime.datetime.now(),
                        "article_versions": [vars(version)],
                        "latest": vars(version),
                        "version_count": 1,
                    }
                )
            else:
                latest_version = ArticleVersion(stored_article["latest"])
                if version != latest_version:
                    (
                        version.total_similarity,
                        version.similarities,
                    ) = version.get_similarity(latest_version)
                    stored_versions = stored_article["article_versions"]
                    collection.update_one(
                        {"url": url},
                        {
                            "$set": {
                                "last_modified": datetime.datetime.now(),
                                "article_versions": stored_versions + [vars(version)],
                                "latest": vars(version),
                                "version_count": len(stored_versions) + 1,
                            }
                        },
                    )
                    print(url, len(stored_versions))
        except Exception as e:
            print(e)

    def format_url(self, url):
        return url
