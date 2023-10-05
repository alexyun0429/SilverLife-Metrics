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

""" 
    database.py initialising code

    Init database connection when the app gets loaded.
    See crtlshiftdelAPI - where after the app is initialised, then this file is called
"""
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'b004cb4920073d576ef69425'
app.config['MYSQL_DB'] = 'hagrid'
mysql = MySQL(app)



"""HELPER CLASSES"""

"""
def addData(data)
Parameters: data - an array of tuples, formatted to directly insert into the database

This function loops through the array of tuples, and for each one, inserts it into the database,
Has minor error handling when inserting, if error on insert, aborts the insert and does not retry adding

Returns 200
"""
def addData(data):
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
    path = f"/var/www/uwsgi/writable/patient_photos/{uat}/"
    os.mkdir(path)
    photo_loction = path + "rest.png"
    photo_upload.save(photo_loction)

    return photo_loction

"""
    Saves the photo locations to the 'photos' table in the database.

    :param photo_locations: A dictionary containing the user access token and the photo locations.
    :type photo_locations: dict
    """
def addPhotos(photo_locations):
    cursor = mysql.connection.cursor()
    try:
        for expression, photo_location in photo_locations['photos'].items():
            sql = """INSERT INTO photos (user_access_token, photo_location, expression_code)
                     VALUES (%s, %s, %s);"""
            cursor.execute(sql, (photo_locations['uat'], photo_location, expression))
            mysql.connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        mysql.connection.rollback()
    finally:
        cursor.close()

def addPhotos(photo_locations):
    cursor = mysql.connection.cursor()
    try:
        for expression in photo_locations['photos'].keys():
            sql = """INSERT INTO photos (photo_id, user_access_token, photo_location, expression_code)
                     VALUES (%s, %s, %s, %s);"""
            cursor.execute(sql, (None, photo_locations['uat'], photo_locations['photos'][expression], expression))
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
    expressions = [0, 1, 2] # We already have a 4th (default photo) # 0 - teethy smile
                                                                    # 1 - pout
                                                                    # 2 - sad :(
    returnObject = {"uat": uat}
    
    photo_locations = {
        3: photo_location
    }
    
    actual_expressions = {0 : "smile", 1 : "pout", 2 : "sad"}
    for expression in expressions:
        conn = http.client.HTTPSConnection("www.ailabapi.com")
        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=image_target; filename={0}'.format('file')))

        fileType = mimetypes.guess_type(photo_location)[0] or 'application/octet-stream'
        dataList.append(encode('Content-Type: {}'.format(fileType)))
        dataList.append(encode(''))

        with open(photo_location, 'rb') as f:
            dataList.append(f.read())
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=service_choice;'))

        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        dataList.append(encode(str(expression))) # append our chosen expression 

        dataList.append(encode(""))
        dataList.append(encode('--'+boundary+'--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary),
            'ailabapi-api-key': 'tLcTahCbAXNB5pgc3m9jLH7DIXsRPoyzSrKw3FdGhikjffEPyZdHZQV6eQB541AO'  # added authorization API key here/can be a key from any account doesn't matter  
        }
        conn.request("POST", "/api/portrait/effects/emotion-editor", payload, headers)
        res = conn.getresponse()
        data = res.read()
        #print(data.decode("utf-8"))

        # Convert bytes to string and parse as JSON
        response_json = json.loads(data.decode("utf-8"))
        #print(response_json)

        # Decode the base64 image data
        try: 
            img_data = base64.b64decode(response_json['data']['image'])
            # Save them under /writable/patient_photos/{uat}/
            directory = f"/var/www/uwsgi/writable/patient_photos/{uat}/"

            file_path = directory + f"photo_{actual_expressions[expression]}.png"

            with open(file_path, "xb") as file:
                file.write(img_data)

            photo_locations[expression] = file_path
        except:
            #failed
            pass

    returnObject["photos"] = photo_locations
    return returnObject


"""TESTING FUNCTIONS"""

"""
    TODO: Delete before go live

    Change call these functions to test above code if needed, just change the code as needed to call specific functions

"""

def get_patients_by_floor(floor_number):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM patients WHERE LEFT(room_number, 1) = %s", (floor_number,))
    data = cursor.fetchall()
    cursor.close()
    # Convert tuples to dictionaries
    patients = []
    for patient_tuple in data:
        patient_dict = {
            "user_access_token": patient_tuple[0],
            "first_name": patient_tuple[1],
            "last_name": patient_tuple[2],
            "room_number": patient_tuple[3]
        }
        patients.append(patient_dict)
    
    return patients

@app.route('/getData', methods=["GET"])
def get_patients():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    cursor.close()
    return data

@app.route('/updateData', methods=["GET"])
def updateData():
    
    return savePhotos(None) # NO savePhotos function
    # return {"data":temp}

