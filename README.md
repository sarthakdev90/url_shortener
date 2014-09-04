url_shortener
=============

A basic url shortener with Flask


Installing Dependencies
=======================

pip install -r requirements.txt


Usage
=====

gunicorn -w 2 api:app

Check the port it's running on, it'll be 8000 in most cases
The POST request should go to that port of the localhost.
The content-type must be 'application/json' and the URL needs be present as value to the key 'url'.


Analytics
=========
The analytics are collected in the Click table present in models.py
