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

"""
    This file is run to initialise the flask app. This is because this file is set as the main file in the uwsgi config file.
    If files need to access the 'app' variable, they need to be imported after 'app' is declared.

    However, if a file is used as a helper, they can be imported above.
"""


app = Flask(__name__, static_url_path="/static")

import ctrlshiftdelFrontEnd
from databaseManip.database import *


"""This function can be ignored, but don't delete"""


@app.route("/")
def index():
    app.logger.info("Info level log")
    app.logger.warning("Warning level log")
    return "<span style='color:red'>Hello index world</span>"


"""This function can be ignored, but don't delete"""


@app.route("/foobar")
def foobar():
    return "<span style='color:blue'>Hello again!</span>"


"""
This function is the webhook used by garmin.
"""


@app.route("/api/stress", methods=["POST"])
def stess():
    data = convertDataTime(request.data)

    addStressData(data)

    # addData(data)
    # print(request.headers, file=sys.stdout, flush=True)
    # print(request.url, file=sys.stdout, flush=True)
    # print(request.data, file=sys.stdout, flush=True)
    request.close()
    return {"data": "success"}


@app.route("/api/hrv", methods=["POST"])
def hrv():
    data = convertDataTime(request.data)

    addHRVData(data)
    request.close()
    return {"data": "success"}


@app.route("/api/hmac")
def hmac():
    data = request.data
    return jsonify({"data": "test"})


""" @app.route('/api/photo', methods = ['POST'])
def photo():
    data = json.loads(str(request.data, encoding='utf-8'))
    uat = data['uat']
    photoLoc = data['photoLocation']
    generatePhotos(uat, photoLoc)
    return {'data': 'success'} """


@app.route("/api/addPatient", methods=["POST"])
def add_patient():
    # print(request.files['photo_upload'], file=sys.stdout, flush=True)
    user_access_token = request.form.get("user_access_token")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    room_name = request.form.get("room_name")
    photo_upload = request.files["photo_upload"]

    patient = addPatient(user_access_token, first_name, last_name, room_name)
    if not patient:
        # Patient already in db
        return
    photo_location = saveDefaultPhoto(user_access_token, photo_upload)
    if photo_location == None:
        # error in the saveDefaultPhoto func
        return

    obj = generatePhotos(user_access_token, photo_location)
    # print(obj['photos'].keys(), file=sys.stdout, flush=True)
    addPhotos(obj)

    return jsonify({"status": "success"})


# Generate folder using ID as folder's name
