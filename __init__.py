from flask import Flask, render_template, request, session, url_for, redirect
import hashlib

import psycopg2

from passlib.hash import sha256_crypt
import datetime

app = Flask(__name__)

#configure postgreSQL
try:
    conn = psycopg2.connect(database="code", user="bc1691",password="StarszndFaults", host="0.0.0.0", port=55432)
except:
    print "Disaster"
#cur = conn.cursor()

@app.route("/")
def hello():
    return "IT'S WORKING THE WORLD SAYS HELLO."
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9800)
