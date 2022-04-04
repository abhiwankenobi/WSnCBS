#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify

records = {}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def query_records():
    id = request.args.get('id')
    if id is not None:
        return records[id]
    else:
        return records

@app.route('/', methods=['PUT'])
def create_record():
    id = request.args['id']
    url = request.args['url']
    records[id] = url
    return ""

@app.route('/', methods=['POST'])
def create_short_url():
    url = request.args['url']
    id = str(hash(url))
    records[id] = url
    return id
    check_url(url)

def check_url(str1):
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    url_compile = re.compile(str1)
    if(re.search(url_compile,str1)):
        return True
    else:
        print("enter correct url")

@app.route('/', methods=['DELETE'])
def delte_record():
    id = request.args['id']
    del records[id]
    return ""

app.run(debug=True)
