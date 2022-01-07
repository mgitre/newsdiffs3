import re
import datetime
from bs4 import BeautifulSoup
from utils.request_utils import getHTML
from utils.database_utils import get_article_urls_within_time, get_database, get_article
from models.article import ArticleVersion


class BaseScraper:
    def __init__(self):
        self.content_exclusions = []
    # gets urls to scrape by scraping a set of base pages

    def get_articles_from_pages(self, pages):
        articles = []
        for starting_page in pages:
            # gets a soup object for the initial page
            homepage_soup = BeautifulSoup(
                getHTML(starting_page), features="lxml")
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
        # add days=x to change how many days to look back
        articles = get_article_urls_within_time(collection)
        return articles

    # gets articles from scraping and from database, and merges them.
    def get_articles(self):
        from_pages = self.get_articles_from_pages(self.starting_pages)
        from_database = self.get_articles_from_database()
        # oh sets, never change
        articles = from_pages + list(set(from_database) - set(from_pages))
        return articles

    # updates url of database entry
    def update_url(self, old_url, new_url):
        collection = get_database()[self.name]
        # if the new url is already in the database, delete the key
        # for the old url and tell the processing function to not scrape it
        if collection.find_one({"url": new_url}):
            print(old_url, new_url, "already exists")
            ##TODO: MERGING
            collection.delete_one({"url": old_url})
            return True
        # if it's not already in the database, change the url to the new url
        # and tell the processing function to continue scraping
        collection.update_one({"url": old_url}, {"$set": {"url": new_url}})
        print(old_url, new_url, "doesnt already exist, adding")
        return False

    # fixes html formatting
    def html_fix(self, text):
        return text.replace("<", "&lt").replace(">", "&gt")

    def process_article(self, url):
        # when in doubt, try/except the whole function
        try:
            # makes a soup object for the article
            html = getHTML(url)
            soup = BeautifulSoup(html, features="lxml")

            # sees if og:url is different from scraped url
            old_url = url
            url = soup.find("meta", property="og:url").attrs['content']
            if url != old_url:
                # if so, try to update the url. if new url already exists, cancel
                new_url_exists = self.update_url(old_url, url)
                if new_url_exists:
                    return

            # get the headline
            headline = None
            for name, attrs in self.headline_matches:
                match_attempt = soup.find(name, attrs)
                if match_attempt:
                    headline = self.html_fix(match_attempt.get_text())
                    break
            # get the subhead
            subhead = None
            for name, attrs in self.subhead_matches:
                match_attempt = soup.find(name, attrs)
                if match_attempt:
                    subhead = self.html_fix(match_attempt.get_text())
                    break
            # get the byline
            byline = None
            for name, attrs, parent in self.byline_matches:
                matchAttempt = soup.find(name, attrs)
                if matchAttempt:
                    if parent:
                        bylinesoup = matchAttempt.parent
                    else:
                        bylinesoup = matchAttempt
                    # fix to get rid of annoying extra text
                    for hidden in bylinesoup.find_all(attrs={"class": "hidden"}):
                        hidden.decompose()
                    # this is ugly but so are a lot of bylines, so....
                    byline = bylinesoup.get_text().replace(u"\xa0", " ").strip()
                    byline = re.sub(r"\s+", " ", byline)
                    byline = self.html_fix(byline)
                    break
            # get the content
            content = None
            for name, attrs in self.content_matches:
                articlebody = soup.find(name, attrs)
                # if it actually finds an article body
                if articlebody:
                    #exclusions = []
                    for arguments in self.content_exclusions:
                        for element in articlebody.find_all(*arguments):
                            element.decompose()
                    paragraphs = []
                    # search for any text tags
                    for paragraph in articlebody.find_all(
                        ["p", "h1", "h2", "h3", "h4", "h5", "h6"]
                    ):
                        text = self.html_fix(paragraph.get_text())
                        # all caps paragraphs are almost always in-article ads
                        # (eg CLICK HERE TO READ THIS OTHER ARTICLE WE WROTE)
                        if text == text.upper():
                            continue
                        # after read more, stop checking
                        if text == "Read more:":
                            break
                        # add to paragraphs
                        paragraphs.append(
                            "<{0}>{1}</{0}>".format(paragraph.name, text)
                        )
                    # join paragraphs by newlines
                    content = "\n".join(paragraphs)
                    break
            # make an articleversion object because we like those
            return ArticleVersion(
                {
                    "headline": headline,
                    "subhead": subhead,
                    "byline": byline,
                    "content": content,
                }
            )
        except Exception as e:
            print(url, "had error", e)

    def update_article(self, url, version):
        # if version is none, give up
        if not version:
            return
        # try/except everything, nothing but best practices here
        try:
            collection = get_database()[self.name]
            # tries to load stored article
            stored_article = get_article(collection, url)
            # if it doesnt exist, create it
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
            # if it does exist, check to see if version is the same as latest version
            else:
                latest_version = ArticleVersion(stored_article["latest"])
                # if not the same, then do similarity calculations and update
                if version != latest_version:
                    if len(stored_article['article_versions']) >= 2 and \
                        version == ArticleVersion(stored_article['article_versions'][-2]):
                        # skip weird issue where different article versions show up
                        print(url, "DUPE BUT WEIRD")
                        if (datetime.datetime.utcnow()-stored_article['article_versions'][-2]['datetime'])\
                            <= datetime.timedelta(minutes=75):
                            return

                    # save similarity info
                    version.total_similarity, version.similarities = version.get_similarity(
                        latest_version)
                    stored_versions = stored_article["article_versions"]
                    # update entry
                    collection.update_one(
                        {"url": url},
                        {
                            "$set": {
                                "last_modified": datetime.datetime.utcnow(),
                                "article_versions": stored_versions + [vars(version)],
                                "latest": vars(version),
                                "version_count": len(stored_versions) + 1,
                            }
                        },
                    )
                    print(url, len(stored_versions))
                    return version, len(stored_versions)
        except Exception as e:
            print(e)

    # default. when needed, add a function to do this better
    def format_url(self, url):
        return url
