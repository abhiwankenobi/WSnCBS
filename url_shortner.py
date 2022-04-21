#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify, redirect
import re
from urllib.parse import urlparse
import datetime
import jwt

SECRET_KEY = "SECRET"
ALGORITHM = "HS256"

def encode_auth_token(username,password):
    """
    Generates the Auth Token
    params: username,password
    return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=300),
            'iat': datetime.datetime.utcnow(),
            'username': username,
            'password': password
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    param: auth_token:
    return: dict
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY,[ALGORITHM])
        #print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired.'
    except jwt.InvalidTokenError:
        return 'Invalid token.'




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


all_records = {}
users = {}



app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_all_ids():
    auth_token = request.headers.get('auth_token')
    auth_user = decode_auth_token(auth_token)
    if isinstance(auth_user, str):
        return (auth_user,403)
    if auth_user['username'] in users.keys():
        return users[auth_user['username']][1]

@app.route('/<id>', methods=['GET'])
def get_url(id):
    '''auth_token = request.headers.get('auth_token')
    auth_user = decode_auth_token(auth_token)
    if auth_user['username'] not in users.keys():
        return ('',403)'''
    if id is not None:
        if id not in all_records.keys():
            return ("ID NOT FOUND", 404)
        '''if id not in users[auth_user['username']][1]:
            #print(users[auth_user['username']][1])
            return ("", 404)'''
        all_records[id]
        return (redirect(all_records[id]),301)
        #return (redirect(users[auth_user['username']][1][id]),301)
    else:
        #return users[auth_user['username']][1]
        return ("No ID", 404)

@app.route('/', methods=['PUT'])
def update_record():
    id = request.args['id']
    url = request.args['url']
    auth_token = request.headers.get('auth_token')
    auth_user = decode_auth_token(auth_token)
    if isinstance(auth_user, str):
        return (auth_user,403)
    if auth_user['username'] not in users.keys():
        return ('',403)
    if id not in users[auth_user['username']][1]:
        return ("", 404)
    users[auth_user['username']][1][id] = url
    all_records[id] = url
    return ""

@app.route('/', methods=['POST'])
def create_short_url():
    auth_token = request.headers.get('auth_token')
    #print("auth_token: "+auth_token)
    auth_user = decode_auth_token(auth_token)
    #print(auth_user)
    if isinstance(auth_user, str):
        return (auth_user,403)
    if auth_user['username'] not in users.keys():
        return ('',403)
    date = str(datetime.datetime.now())
    #print(date)
    url = request.args['url']
    id = str(hash(url+date))
    #print(check_url(url))
    if check_url(url) is False:
        return ("Please enter a valid url", 400)
    users[auth_user['username']][1][id] = url
    all_records[id] = url
    return request.base_url+str(id)

@app.route('/', methods=['DELETE'])
def delete_record():
    auth_token = request.headers.get('auth_token')
    auth_user = decode_auth_token(auth_token)
    if isinstance(auth_user, str):
        return (auth_user,403)
    if auth_user['username'] not in users.keys():
        return ('',403)
    if len(request.args) == 0:
        for key in users[auth_user['username']][1]:
            del all_records[key]
        users[auth_user['username']][1].clear()
        return ('All records cleared for ' + auth_user['username']+'!',204)
    id = request.args['id']
    if id not in users[auth_user['username']][1]:
        return ("", 404)
    del users[auth_user['username']][1][id]
    del all_records[id]
    return ('', 204)

@app.route('/users', methods=['POST'])
def create_user():
    username = request.args['username']
    password = request.args['password']
    users[username] = []
    users[username].append(password)
    user_records = {}
    users[username].append(user_records)
    return ('',200)

@app.route('/users/login', methods=['POST'])
def login_user():
    username = request.args['username']
    password = request.args['password']
    if users[username] is None:
        return ("Please register first",403)
    if users[username][0] == password:
        users[username].append(str(encode_auth_token(username,password)))
        print(users)
        return (users[username][2],200)
    else:
        return ("Username or password not correct.",403)






app.run(debug=True)
