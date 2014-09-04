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

