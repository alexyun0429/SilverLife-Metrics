from flask import Flask, jsonify, request
from datetime import date
import sys
import json
from databaseManip.restructureStressData import *
from databaseManip.restructureHRVData import *
import logging
import threading
import time
import os

# Module-level Docstring
"""
Flask application initialization module.
This module initializes the Flask application and provides various endpoints for Garmin integration and patient management.
"""


app = Flask(__name__, static_url_path="/static")

# Import necessary components and modules after the app initialization
import ctrlshiftdelFrontEnd
from databaseManip.database import *


@app.route("/")
def index():
    """
    Test route for checking Flask application deployment.
    This route logs messages and returns a red-styled message.
    """
    app.logger.info("Info level log")
    app.logger.warning("Warning level log")
    return "<span style='color:red'>Hello index world</span>"


@app.route("/foobar")
def foobar():
    """
    Another test route.
    This can be used for various checks during development.
    """
    return "<span style='color:blue'>Hello again!</span>"


@app.route("/api/stress", methods=["POST"])
def stress():
    """
    Webhook endpoint for Garmin stress data.
    Accepts POST requests containing stress data, processes and stores the data in the database.
    """
    data = convertStressDataSet(
        request.data
    )  # Convert the received data into the desired format
    addStressData(data)  # Store the processed data in the database
    request.close()
    return {"data": "success"}


@app.route("/api/hrv", methods=["POST"])
def hrv():
    """
    Webhook endpoint for Garmin HRV (Heart Rate Variability) data.
    Accepts POST requests containing HRV data, processes and stores the data in the database.
    """
    data = convertHrvDataSet(
        request.data
    )  # Convert the received data into the desired format
    addHRVData(data)  # Store the processed data in the database
    request.close()
    return {"data": "success"}


@app.route("/api/hmac")
def hmac():
    """
    Placeholder route for HMAC verification.
    Currently, it just returns a JSON with test data.
    """
    data = request.data
    return jsonify({"data": "test"})


@app.route("/api/addPatient", methods=["POST"])
def add_patient():
    """
    Endpoint to add a new patient.
    Accepts POST requests containing patient details and their photo.
    """
    try:
        user_access_token = request.form.get("user_access_token")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        room_number = request.form.get("room_number")
        photo_upload = request.files["photo_upload"]

        photo_location = saveDefaultPhoto(user_access_token, photo_upload)

        if photo_location is None:  # Check for errors during photo save
            return (
                jsonify({"status": "error", "message": "Failed to save default photo"}),
                500,
            )

        patient = addPatient(user_access_token, first_name, last_name, room_number)

        if patient:  # Check if the patient already exists
            return (
                jsonify({"status": "error", "message": "Patient already in database"}),
                400,
            )

        obj = generatePhotos(user_access_token, photo_location)
        addPhotos(obj)
        return jsonify({"status": "success"})

    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr, flush=True)
        return jsonify({"status": "error", "message": str(e)}), 500

        # print(obj["photos"].keys(), file=sys.stdout, flush=True)
