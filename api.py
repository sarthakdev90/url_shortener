from flask import Flask, jsonify, request, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import os, json
import base64
import redis, re
from helpers import is_url, add_to_redis

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.name = 'short.url'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'test.db')

red = redis.Redis()

@app.route('/', methods=['POST'])
def shorten():

   data = json.loads(request.data)
   url = data['url'].strip()
   if not is_url(url):
    return jsonify({'error': 'Not a valid url'})

   key = base64.b64encode(url)[-6:].replace('=','')
   add_to_redis(red, key, url)

   url = url_for('bounce', key=key, _external=True)
   return jsonify({'url': url})

@app.route('/<key>', methods=['GET'])
def bounce(key):
    try:
        data = red.hgetall('urls')
        url = data.get('key')
        return redirect(url)
    except KeyError as e:
        return jsonify({'error': 'url not found'}, 400)

if __name__ == '__main__':
    app.run()
