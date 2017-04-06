
from flask import Flask, render_template, request, session, url_for, redirect
import hashlib

import psycopg2

from passlib.hash import sha256_crypt
import datetime

app = Flask(__name__)

#configure postgreSQL
conn_string = "host='0.0.0.0' dbname='bc1691' user='bc1691' password='StarszndFaults'"
print "Connecting..."
conn = psycopg2.connect(conn_string)

print "Connected\n"
#cur = conn.cursor()

@app.route("/")
def index():
    cursor = conn.cursor()
    query = 'SELECT * FROM petmodel ORDER BY pet_name ASC'
    cursor.execute(query)
    
    data = cursor.fetchone()
    if(data):
        print data
    cursor.close();
    
    return "IT'S WORKING I AM GETTING STRONGER."

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['Username']
    password = request.form['Password']
    
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT password FROM UserAccount WHERE username = %s'
    cursor.execute(query, (username,))
    
    #stores the results in a variable
    data = cursor.fetchone()
    if(not data):
        error = 'Invalid login or username'
        return error
    #use fetchall() if you are expecting more than 1 data row
    
    cursor.close()
    error = None

	_username, _password, _email, _created_on, _last_login = data
    if(sha256_crypt.verify(password, _password)):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('index'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return error

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['Username']
    password = request.form['Password']
    email = request.form['email']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
    password2 = sha256_crypt.encrypt(password)
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM UserAccount WHERE username = %s'
    cursor.execute(query, (username,))
    
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return error
    else:
        ins = 'INSERT INTO UserAccount VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password2, email, timestamp, timestamp))
        conn.commit()
        cursor.close()
        return redirect(url_for('index'))

def logout():
    session.pop('username')
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9800)
	
