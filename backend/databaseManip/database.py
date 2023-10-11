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

""" 
    database.py initialising code

    Init database connection when the app gets loaded.
    See crtlshiftdelAPI - where after the app is initialised, then this file is called
"""

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


"""
def addStressData(data)
Parameters: data - an array of tuples, formatted to directly insert into the database

This function loops through the array of tuples, and for each one, inserts it into the database,
Has minor error handling when inserting, if error on insert, aborts the insert and does not retry adding

Returns 200
"""


def addHRVData(data):
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


"""
    Adds a new patient record to the 'patients' table in the database.

    :param user_access_token: The unique token identifying the user.
    :type user_access_token: str
    :param first_name: The first name of the patient.
    :type first_name: str
    :param last_name: The last name of the patient.
    :type last_name: str
    :param room_name: The name of the room assigned to the patient.
    :type room_name: str
    """


def addPatient(user_access_token, first_name, last_name, room_name):
    cursor = mysql.connection.cursor()
    error = False
    try:
        sql = """INSERT INTO patients (user_access_token, first_name, last_name, room_number)
                 VALUES (%s, %s, %s, %s);"""
        cursor.execute(sql, (user_access_token, first_name, last_name, room_name))
        mysql.connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        error = True
        mysql.connection.rollback()
    finally:
        cursor.close()
        return error


def saveDefaultPhoto(uat, photo_upload):
    # Need to create patient folder
    path = f"/var/www/uwsgi/static/patient_photos/{uat}/"
    os.mkdir(path)
    photo_loction = path + "1.png"
    photo_upload.save(photo_loction)

    return photo_loction


"""
    Saves the photo locations to the 'photos' table in the database.

    :param photo_locations: A dictionary containing the user access token and the photo locations.
    :type photo_locations: dict
    """
# def addPhotos(photo_locations):
#     cursor = mysql.connection.cursor()
#     try:
#         for expression, photo_location in photo_locations['photos'].items():
#             sql = """INSERT INTO photos (user_access_token, photo_location, expression_code)
#                      VALUES (%s, %s, %s);"""
#             cursor.execute(sql, (photo_locations['uat'], photo_location, expression))
#             mysql.connection.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#         mysql.connection.rollback()
#     finally:
#         cursor.close()


def addPhotos(photo_locations):
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
            3: photo_location_string,    #the location of the photo
            0: photo_location_string,
            1: photo_location_string,
            2: photo_location_string
        }
    }
"""


def generatePhotos(uat, photo_location):
    # Call AILabs to get the expression photos
    expressions = [0, 2]
    # 0 - teethy smile => low
    # 1 - default => rest
    # 2 - sad => high

    returnObject = {"uat": uat}

    photo_locations = {3: photo_location}

    actual_expressions = {0: "0", 2: "2", 1: "1"}
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
    cursor = None

    # 1) Get patient's by floor
    # 2) Get most recent stress data row per patient
    # 3) Retrieve correct photo path depending on stress status
    # 4) Make into dictionary and return.
    # *) every 5min re render
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
                    (s.stress_status = 'Low' AND ph.expression_code = 0) OR
                    (s.stress_status = 'Rest' AND ph.expression_code = 1) OR
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

        print(data, file=sys.stdout, flush=True)
        return patients
    except Exception as e:
        print(f"Error: {str(e)}")
        return []
    finally:
        if cursor:
            cursor.close()


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
