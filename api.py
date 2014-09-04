from flask import Flask, jsonify, request, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import os, json
import base64
import redis, re

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.name = 'short.url'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+basedir+'/click.db'
app.debug = True

red = redis.Redis()
red_count = redis.Redis(db=1)
db = SQLAlchemy(app)

@app.route('/', methods=['POST'])
def shorten():
    '''
    Code to receive the request for shortening a URL
    '''
    if not request.data:
        return jsonify({'error': 'Did not receive data'})

    data = json.loads(request.data)
    url = data['url'].strip()

    if not helpers.is_url(url):
        return jsonify({'error': 'Not a valid url'})

    key = base64.b64encode(url)[-6:].replace('=','')
    helpers.add_to_redis(red, key, url)

    url = url_for('bounce', key=key, _external=True)
    return jsonify({'url': url, 'pass': True})

@app.route('/<key>', methods=['GET'])
def bounce(key):
    try:
        data = red.hgetall('urls')
        url = data.get(key)
        helpers.increment_counter(red_count, key) #Increment counter in redis
        helpers.store_headers(request.headers, key) #Add to analytics db

        return redirect(url)
    except KeyError as e:
        return jsonify({'error': 'url not found'}, 400)


import helpers, models
