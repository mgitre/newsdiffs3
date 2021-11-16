from typing import get_args
from flask import Flask, render_template, abort, redirect, request, jsonify
from bson.json_util import dumps
import json
import re
import yaml
from utils.database_utils import get_article, get_database


app = Flask(__name__)

with open("config.yaml") as f:
    config = yaml.safe_load(f)['SERVER']

base_url = config['PUBLIC_URL']
host = config['HOST']
port = config['PORT']

@app.route('/<site>/<path:article>')
def articleView(site, article):
    return render_template("index.html", site=site, url=article)

@app.route('/api', methods=['POST'])
def do_api_shit():
    req=json.loads(request.data)
    url = req['url']
    site = req['site']
    collection = get_database()[site]
    return dumps(get_article(collection, url))

app.run(port=port, host=host)