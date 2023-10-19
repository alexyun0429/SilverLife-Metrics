from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from ctrlshiftdelAPI import app
import http.client
import mimetypes
from codecs import encode
import base64
from io import BytesIO
import json
import os
import sys
from datetime import date, timedelta, datetime, time
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import io
import base64


# database.py initialising code

# Init database connection when the app gets loaded.
# See crtlshiftdelAPI - where after the app is initialised, then this file is called


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "b004cb4920073d576ef69425"
app.config["MYSQL_DB"] = "hagrid"
mysql = MySQL(app)


"""HELPER CLASSES"""

"""
def addStressData(data)
Parameters: data - an array of tuples, formatted to directly insert into the database

This function loops through the array of tuples, and for each one, inserts it into the database,
Has minor error handling when inserting, if error on insert, aborts the insert and does not retry adding

Returns 200
"""


def addStressData(data):
    """
    Insert stress data into a MySQL database table.

    Args:
        data (list): A list of stress data items. Each item should be a tuple containing the following values in order: stress_id, user_access_token, local_date, local_time, stress_level_value, stress_status.

    Returns:
        int: A status code indicating the success of the function. (200)

    Example Usage:
        data = [
            (1, 'token1', '2021-01-01', '10:00:00', 5, 'high'),
            (2, 'token2', '2021-01-02', '11:00:00', 3, 'medium'),
            (3, 'token3', '2021-01-03', '12:00:00', 2, 'low')
        ]
        result = addStressData(data)
        print(result)  # Output: 200
    """
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO stress (stress_id, user_access_token, local_date, local_time, stress_level_value, stress_status) VALUES (%s, %s, %s, %s, %s, %s);"
    for i in data:
        try:
            cursor.execute(sql, i)
            mysql.connection.commit()
        except:
            mysql.connection.rollback()

    cursor.close()
    return 200


def addHRVData(data):
    """
    def addHRVData(data)
    Parameters: data - an array of tuples, formatted to directly insert into the database

    This function loops through the array of tuples, and for each one, inserts it into the database,
    Has minor error handling when inserting, if error on insert, aborts the insert and does not retry adding

    Returns 200
    """
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO hrv (hrv_id, user_access_token, local_date, local_time, hrv_value) VALUES (%s, %s, %s, %s, %s, %s);"
    for i in data:
        try:
            cursor.execute(sql, i)
            mysql.connection.commit()
        except:
            mysql.connection.rollback()

    cursor.close()
    return 200


def addPatient(user_access_token, first_name, last_name, room_number):
    """
    Adds a new patient record to the 'patients' table in the database.

    :param user_access_token: The unique token identifying the user.
    :type user_access_token: str
    :param first_name: The first name of the patient.
    :type first_name: str
    :param last_name: The last name of the patient.
    :type last_name: str
    :param room_number: The name of the room assigned to the patient.
    :type room_number: str
    """
    cursor = mysql.connection.cursor()
    error = False
    try:
        sql = """INSERT INTO patients (user_access_token, first_name, last_name, room_number)
                 VALUES (%s, %s, %s, %s);"""
        cursor.execute(sql, (user_access_token, first_name, last_name, room_number))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error in db.py addPatient: {e}", file=sys.stdout, flush=True)
        error = True
        mysql.connection.rollback()
    finally:
        cursor.close()
        return error


def saveDefaultPhoto(uat, photo_upload):
    """
    Create a folder for a patient using a user access token and save a default photo in that folder.

    Args:
        uat (str): The user access token used to create the patient folder.
        photo_upload (file): The photo file to be saved.

    Returns:
        str: The location where the default photo is saved.
    """
    # Create patient folder using user access token
    path = f"/var/www/uwsgi/static/patient_photos/{uat}/"
    os.mkdir(path)
    photo_loction = path + "1.png"
    photo_upload.save(photo_loction)

    return photo_loction


def addPhotos(photo_locations):
    """
    Saves the photo locations to the 'photos' table in the database.

    :param photo_locations: A dictionary containing the user access token and the photo locations.
    :type photo_locations: dict
    """
    cursor = mysql.connection.cursor()
    try:
        for expression in photo_locations["photos"].keys():
            sql = """INSERT INTO photos (photo_id, user_access_token, photo_location, expression_code)
                     VALUES (%s, %s, %s, %s);"""
            cursor.execute(
                sql,
                (
                    None,
                    photo_locations["uat"],
                    photo_locations["photos"][expression],
                    expression,
                ),
            )
            mysql.connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        mysql.connection.rollback()
    finally:
        cursor.close()


def generatePhotos(uat, photo_location):
    """
    def generatePhotos(uat, photo_location)
    PARAMETERS:
    uat - the User Access Token (Patient Primary key)
    photo_location - the location of the original patient photo - needs to be loaded in the patients folder in writable already

    This function generates an AI photo from the original patient photo for each expressions (see below for list)
    It then saves each photo under the patients writable folder

    RETURNS:
    An object of the format:
        returnObject = {
            "uat": uat,      #the uat of the patient
            "photos": {
                0: photo_location_string,
                1: photo_location_string,
                2: photo_location_string
            }
        }
    """
    # Call AILabs to get the expression photos
    expressions = [0, 2, 3]
    # 0 - teethy smile => low
    # 1 - default => rest
    # 2 - sad => high
    # 3 - genetle smile => medium

    returnObject = {"uat": uat}

    photo_locations = {3: photo_location}

    actual_expressions = {0: "0", 2: "2", 1: "1", 3: "3"}
    for expression in expressions:
        conn = http.client.HTTPSConnection("www.ailabapi.com")
        dataList = []
        boundary = "wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T"
        dataList.append(encode("--" + boundary))
        dataList.append(
            encode(
                "Content-Disposition: form-data; name=image_target; filename={0}".format(
                    "file"
                )
            )
        )

        fileType = mimetypes.guess_type(photo_location)[0] or "application/octet-stream"
        dataList.append(encode("Content-Type: {}".format(fileType)))
        dataList.append(encode(""))

        with open(photo_location, "rb") as f:
            dataList.append(f.read())
        dataList.append(encode("--" + boundary))
        dataList.append(encode("Content-Disposition: form-data; name=service_choice;"))

        dataList.append(encode("Content-Type: {}".format("text/plain")))
        dataList.append(encode(""))
        dataList.append(encode(str(expression)))  # append our chosen expression

        dataList.append(encode(""))
        dataList.append(encode("--" + boundary + "--"))
        dataList.append(encode(""))
        body = b"\r\n".join(dataList)
        payload = body
        headers = {
            "Content-type": "multipart/form-data; boundary={}".format(boundary),
            "ailabapi-api-key": "tLcTahCbAXNB5pgc3m9jLH7DIXsRPoyzSrKw3FdGhikjffEPyZdHZQV6eQB541AO",  # added authorization API key here/can be a key from any account doesn't matter
        }
        conn.request("POST", "/api/portrait/effects/emotion-editor", payload, headers)
        res = conn.getresponse()
        data = res.read()
        # print(data.decode("utf-8"))

        # Convert bytes to string and parse as JSON
        response_json = json.loads(data.decode("utf-8"))
        # print(response_json)

        # Decode the base64 image data
        try:
            img_data = base64.b64decode(response_json["data"]["image"])
            # Save them under /writable/patient_photos/{uat}/
            directory = f"/var/www/uwsgi/static/patient_photos/{uat}/"

            file_path = directory + f"{actual_expressions[expression]}.png"

            with open(file_path, "xb") as file:
                file.write(img_data)

            photo_locations[expression] = file_path
        except:
            # failed
            pass

    returnObject["photos"] = photo_locations
    return returnObject


def get_patients_by_floor(floor_number):
    """
    This function retrieves patient data from a database for a given floor number.

    It executes a SQL query to fetch the user access token, first name, last name, room number, and photo path of patients.
    The query also joins with the stress table to get the latest stress status of each patient and the photos table to get the corresponding photo based on the stress status.
    The function returns a list of dictionaries where each dictionary contains details of a patient.

    Parameters:
    floor_number (str): The floor number for which patient data is to be retrieved.

    Returns:
    list: A list of dictionaries where each dictionary contains 'user_access_token', 'first_name', 'last_name', 'room_number', and 'photo_path' of a patient.

    """
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        query = """
                SELECT
                    p.user_access_token, p.first_name, p.last_name, p.room_number, CONCAT('/static/patient_photos/', p.user_access_token, '/', ph.expression_code, '.png') AS photo_path
                FROM
                    patients p
                LEFT JOIN
            (
                SELECT 
                    user_access_token, stress_status,
                    ROW_NUMBER() OVER(PARTITION BY user_access_token ORDER BY local_date DESC, local_time DESC) AS rn
                FROM stress
            ) s ON p.user_access_token = s.user_access_token AND s.rn = 1
        LEFT JOIN
            photos ph ON p.user_access_token = ph.user_access_token AND
                (
                    (s.stress_status = 'Rest' AND ph.expression_code = 1) OR
                    (s.stress_status = 'Low' AND ph.expression_code = 0) OR
                    (s.stress_status = 'Medium' AND ph.expression_code = 3) OR
                    (s.stress_status = 'High' AND ph.expression_code = 2) 
                )
        WHERE
            LEFT(p.room_number, 1) = %s

        """

        cursor.execute(query, (floor_number,))
        data = cursor.fetchall()
        patients = [
            {
                "user_access_token": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "room_number": row[3],
                "photo_path": row[4],
            }
            for row in data
        ]

        # print(data, file=sys.stdout, flush=True)
        return patients
    except Exception as e:
        print(f"Error: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()


def build_graph(x, y):
    """
    Generate a graph with custom formatting based on input data and return its encoded URL.

    Parameters:
    - x (list): A list of dates for the x-axis.
    - y (list): A list of values for the y-axis.

    Returns:
    - str: Base64 encoded URL of the generated graph in PNG format.
    """
    img = io.BytesIO()
    fig, ax = plt.subplots(figsize=(9, 5))
    dates = matplotlib.dates.date2num(x)

    ax.plot_date(dates, y, linestyle="solid", marker="None", color="#7DC8CA")

    # Change the color of the axes and labels
    ax.spines["bottom"].set_color("#D0D5F7")
    ax.spines["bottom"].set_linewidth(2)
    ax.spines["top"].set_color("white")
    # ax.xaxis.label.set_color("red")
    ax.tick_params(axis="x", colors="black")

    ax.spines["left"].set_color("#D0D5F7")
    ax.spines["left"].set_linewidth(2)
    ax.spines["right"].set_color("white")
    # ax.yaxis.label.set_color("blue")
    ax.tick_params(axis="y", colors="black")

    # Rotate date labels
    # plt.gcf().autofmt_xdate()
    fig.autofmt_xdate()

    plt.savefig(img, format="png")
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def build_graph1(x, y):
    """
    Generate a smaller graph with custom formatting based on input data and return its encoded URL.

    Parameters:
    - x (list): A list of dates for the x-axis.
    - y (list): A list of values for the y-axis.

    Returns:
    - str: Base64 encoded URL of the generated graph in PNG format.
    """
    img = io.BytesIO()
    fig, ax = plt.subplots(figsize=(3, 1))
    dates = matplotlib.dates.date2num(x)

    ax.plot_date(dates, y, linestyle="solid", marker="None", color="#7DC8CA")

    # Change the color of the axes and labels
    ax.spines["bottom"].set_color("#D0D5F7")
    ax.spines["bottom"].set_linewidth(2)
    ax.spines["top"].set_color("white")
    # ax.xaxis.label.set_color("red")
    ax.tick_params(axis="x", colors="black")

    ax.spines["left"].set_color("#D0D5F7")
    ax.spines["left"].set_linewidth(2)
    ax.spines["right"].set_color("white")
    # ax.yaxis.label.set_color("blue")
    ax.tick_params(axis="y", colors="black")

    # Rotate date labels
    # plt.gcf().autofmt_xdate()
    fig.autofmt_xdate()

    plt.savefig(img, format="png")
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def generate_graphs_30(patients_data):
    """
    Generate and append a 30-day stress graph for each patient in the input data.

    Parameters:
    - patients_data (list): A list of dictionaries where each dictionary contains patient data
      and the key "user_access_token" used to retrieve stress data from a database.

    Returns:
    - list: Updated list of patient dictionaries with the added key "graph30" containing the encoded graph URL.
    """
    data_types = ["stress"]  # 'hrv', 'sleep'
    new_patients = []

    for patient in patients_data:
        for dtype in data_types:
            x = []
            y = []
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM stress WHERE user_access_token = %s AND local_date >= NOW() - INTERVAL 30 DAY ORDER BY stress_id ASC;"
            try:
                cursor.execute(query, (patient["user_access_token"],))
                data = cursor.fetchall()
                for row in data:
                    midnight = datetime.combine(datetime.today(), time(0))

                    # Add the timedelta to the datetime object and extract the time
                    my_time = (midnight + row[3]).time()
                    timed = datetime.combine(row[2], my_time)

                    # time = datetime.strptime(date_string, '%y-%m-%d %H:%M:%S')
                    x.append(timed)
                    y.append(row[4])
            except Exception as e:
                print(f"Error: {str(e)}")
                mysql.connection.rollback()
            cursor.close()
            patient["graph30"] = build_graph(x, y)
            new_patients.append(patient)

    return new_patients


def generate_graphs_1(patients_data):
    """
    Generate and append a 1-day stress graph for each patient in the input data.

    Parameters:
    - patients_data (list): A list of dictionaries where each dictionary contains patient data
      and the key "user_access_token" used to retrieve stress data from a database.

    Returns:
    - list: Updated list of patient dictionaries with the added key "graph1" containing the encoded graph URL.
    """
    data_types = ["stress"]  # 'hrv', 'sleep'
    new_patients = []

    for patient in patients_data:
        for dtype in data_types:
            x = []
            y = []
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM stress WHERE user_access_token = %s AND local_date >= NOW() - INTERVAL 1 DAY ORDER BY stress_id ASC;"
            try:
                cursor.execute(query, (patient["user_access_token"],))
                data = cursor.fetchall()
                for row in data:
                    midnight = datetime.combine(datetime.today(), time(0))

                    # Add the timedelta to the datetime object and extract the time
                    my_time = (midnight + row[3]).time()
                    timed = datetime.combine(row[2], my_time)

                    # time = datetime.strptime(date_string, '%y-%m-%d %H:%M:%S')
                    x.append(timed)
                    y.append(row[4])
            except Exception as e:
                print(f"Error: {str(e)}")
                mysql.connection.rollback()
            cursor.close()
            patient["graph1"] = build_graph1(x, y)
            new_patients.append(patient)

    return new_patients


"""TESTING FUNCTIONS"""

"""
    TODO: Delete before go live

    Change call these functions to test above code if needed, just change the code as needed to call specific functions

"""


@app.route("/getData", methods=["GET"])
def get_patients():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    cursor.close()
    return data


@app.route("/updateData", methods=["GET"])
def updateData():
    return savePhotos(None)
    # return {"data":temp}
