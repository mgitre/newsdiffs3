import json
import yaml
from flask import Flask, render_template, request, Response
from bson.json_util import dumps
from utils.database_utils import get_article, get_database, get_articles_for_homepage


app = Flask(__name__)

with open("config.yaml") as f:
    config = yaml.safe_load(f)['SERVER']

base_url = config['PUBLIC_URL']
host = config['HOST']
port = config['PORT']


@app.route('/<site>/<path:article>')
def article_view(site, article):
    return render_template("article.html", site=site, url=article)

@app.route('/<path:article>')
def article_view_2(article):
    return render_template("article.html", site='', url=article)

@app.route('/api/article', methods=['POST'])
def do_api_shit():
    req=json.loads(request.data)
    url = req['url']
    site = req['site']
    collection = get_database()['articles']
    return dumps(get_article(collection, url))

@app.route('/api/homepage', methods=['POST'])
def get_homepage():
    req = json.loads(request.data)
    outlets = req['outlets']
    page_length = req['page_length']
    page_num = req['page_num']
    return Response(response=dumps(get_articles_for_homepage(outlets, page_length, page_num)), mimetype="application/json", status=200)

@app.route('/')
def render_index():
    return render_template("index.html")


app.run(port=port, host=host)
