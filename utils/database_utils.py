import datetime
import yaml
from pymongo import MongoClient


def get_database():
    # load config
    with open("config.yaml") as f:
        config = yaml.safe_load(f)["MONGODB"]

    # gets a client
    client = MongoClient(host=config["HOST"], port=config["PORT"])

    db = client[config["DATABASE"]]

    return db


def get_article_urls_within_time(collection, days=7):
    # gets relevant collection
    # collection = database[newspaper]

    # figures out what day the last_modified must be after
    timestamp = datetime.datetime.utcnow() - datetime.timedelta(days=days)

    # finds url of any article that fits those requirements
    articles = collection.find({"last_modified": {"$gt": timestamp}}, {"url": True})

    # returns the url of those
    return [article["url"] for article in articles]


def get_article(collection, url):
    # collection=database[newspaper]
    article = collection.find_one({"url": url})
    return article
