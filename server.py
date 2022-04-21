import json
import yaml
from flask import Flask, render_template, request
from bson.json_util import dumps
from utils.database_utils import get_article, get_database


app = Flask(__name__)

with open("config.yaml") as f:
    config = yaml.safe_load(f)['SERVER']

base_url = config['PUBLIC_URL']
host = config['HOST']
port = config['PORT']

@app.route('/<site>/<path:article>')
def article_view(site, article):
    return render_template("article.html", site=site, url=article)

@app.route('/api/article', methods=['POST'])
def do_api_shit():
    req=json.loads(request.data)
    url = req['url']
    site = req['site']
    collection = get_database()['articles']
    return dumps(get_article(collection, url))

app.run(port=port, host=host)
