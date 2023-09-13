from flask import Flask
from flask import jsonify
from flask import request
from datetime import date
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return "<span style='color:red'>Hello index world</span>"

@app.route('/foobar')
def foobar():
    return "<span style='color:blue'>Hello again!</span>"


@app.route('/api/test', methods = ['POST'])
def test():
    print(request.headers, file=sys.stdout, flush=True)
    print(request.url, file=sys.stdout, flush=True)
    print(request.data, file=sys.stdout, flush=True)
    return request.data


@app.route('/api/hmac')
def hmac():
    data = request.data
    return jsonify({"data":"test"})
