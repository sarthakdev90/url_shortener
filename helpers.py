import re

def is_url(string):
    return re.match('http(s){0,1}://.+\..+', string, re.I) is not None

def add_to_redis(redis_conn, key, url):
    redis_conn.hset('test', key, url)
    return True
