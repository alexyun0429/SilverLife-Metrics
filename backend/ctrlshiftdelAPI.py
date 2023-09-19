from flask import Flask
from flask import jsonify
from flask import request
from datetime import date
import sys
import json
from databaseManip.timestampConverter import *
import logging
import threading
import time
import os


app = Flask(__name__)

import ctrlshiftdelFrontEnd
from databaseManip.database import *

@app.route('/')
def index():
    return "<span style='color:red'>Hello index world</span>"

@app.route('/foobar')
def foobar():
    return "<span style='color:blue'>Hello again!</span>"

@app.route('/api/stress', methods = ['POST'])
def stess():
    
    data = convertDataTime(request.data)
    
    addData(data)

    #addData(data)
    #print(request.headers, file=sys.stdout, flush=True)
    #print(request.url, file=sys.stdout, flush=True)
    #print(request.data, file=sys.stdout, flush=True)
    request.close()
    return {"data": "success"}

@app.route('/api/hmac')
def hmac():
    data = request.data
    return jsonify({"data":"test"})

