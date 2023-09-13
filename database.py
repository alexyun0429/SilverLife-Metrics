from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'b004cb4920073d576ef69425'
app.config['MYSQL_DB'] = 'hagrid'

def addDate(data):
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
    mysql.connection.commit()
    cursor.close()
 
mysql = MySQL(app)