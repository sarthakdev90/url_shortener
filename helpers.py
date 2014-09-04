import re
from ua_parser import user_agent_parser
from datetime import datetime
from models import db, Click

def is_url(string):
    return re.match('http(s){0,1}://.+\..+', string, re.I) is not None

def add_to_redis(redis_conn, key, url):
    redis_conn.hset('urls', key, url)
    return True

def check_redis(redis_conn, key):
    data = redis_conn.hgetall('urls')
    return data.get(key)

def increment_counter(redis_conn, key):
    if not redis_conn.get(key):
        redis_conn.set(key, 1)
    else:
        count = redis_conn.incr(key)

def store_headers(headers, key):
    user_agent = user_agent_parser.Parse(headers.get('User-Agent'))
    ip = headers.get('X-Forwarded-For')
    device = user_agent['device'].get('family')
    os = user_agent['os'].get('family')

    print "here"
    click = Click(id = 1, ip = ip, device = device, os = os, timestamp = datetime.now())

    db.session.add(click)
    db.session.commit()

