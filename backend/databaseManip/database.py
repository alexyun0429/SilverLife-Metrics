from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from ctrlshiftdelAPI import app
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'b004cb4920073d576ef69425'
app.config['MYSQL_DB'] = 'hagrid'
mysql = MySQL(app)

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


# # this is the code for timestampConverter.py
# for record in data:
#     add_stress = ("INSERT INTO stress "
#                   "(user_access_token, local_date, local_time, stress_level_value, stress_status) "
#                   "VALUES (%s, %s, %s, %s, %s)")
#     cursor.execute(add_stress, (record['User Access Token'], record['Local Date'], record['Local Time'], record['Stress Level Value'], record['Stress Status']))

@app.route('/getData', methods=["GET"])
def retrieveData_test():
    cursor = mysql.connection.cursor()
    operation = "SELECT * FROM patients"
    cursor.execute(operation)
    temp = cursor.fetchall()[0]
    cursor.close()
    return {"data":temp}

@app.route('/updateData', methods=["GET"])
def updateData():
    temp = "fuck off"
    return {"data":temp}




# mysql = MySQL(app)
# retrieveData_test()

