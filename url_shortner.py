#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify, redirect
import re
from urllib.parse import urlparse

def check_url(str1):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, str1) is not None:
        return True
    else:
        return False


records = {}


app = Flask(__name__)

@app.route('/', methods=['GET'])
def query_records():
    id = request.args.get('id')
    if id not in records:
        return ("", 404)
    if id is not None:
        return (redirect(records[id]),301)
    else:
        return records

@app.route('/', methods=['PUT'])
def create_record():
    id = request.args['id']
    url = request.args['url']
    if id not in records:
        return ("", 404)
    records[id] = url
    return ""

@app.route('/', methods=['POST'])
def create_short_url():
    url = request.args['url']
    id = str(hash(url))
    print(check_url(url))
    if check_url(url) is False:
        return ("Please enter a valid url", 400)
    records[id] = url
    return id

@app.route('/', methods=['DELETE'])
def delte_record():
    id = request.args['id']
    if id not in records:
        return ("", 404)
    del records[id]
    return ('', 204)



app.run(debug=True)
