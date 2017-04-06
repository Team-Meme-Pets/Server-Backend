
from flask import Flask, render_template, request, session, url_for, redirect
import hashlib

import psycopg2

from passlib.hash import sha256_crypt
import datetime

app = Flask(__name__)

#configure postgreSQL
conn_string = "host='0.0.0.0' dbname='code' user='bc1691' password='StarszndFaults'"
print "Connecting..."
conn = psycopg2.connect(conn_string)

print "Connected\n"
#cur = conn.cursor()

@app.route("/")
def hello():
    cursor = conn.cursor()
    query = 'SELECT * FROM petmodel ORDER BY pet_id ASC'
    cursor.execute(query)
    
    data = cursor.fetchone()
    if(data):
        print data
    cursor.close();
    
    return "IT'S WORKING THE WORLD SAYS HELLO."
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9800)
