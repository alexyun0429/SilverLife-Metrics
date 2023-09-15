from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'b004cb4920073d576ef69425'
app.config['MYSQL_DB'] = 'hagrid'

def addData(data):
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
    mysql.connection.commit()
    cursor.close()
# # this is the code for my timestampConverter.py
# for record in data:
#     add_stress = ("INSERT INTO stress "
#                   "(user_access_token, local_date, local_time, stress_level_value, stress_status) "
#                   "VALUES (%s, %s, %s, %s, %s)")
#     cursor.execute(add_stress, (record['User Access Token'], record['Local Date'], record['Local Time'], record['Stress Level Value'], record['Stress Status']))

def retrieveData_test():
    cursor = mysql.connection.cursor()
    a = cursor.execute("""SELECT * FROM patients""")
    print(a.fetchall())

#mysql = MySQL(app)
#retrieveData_test()

