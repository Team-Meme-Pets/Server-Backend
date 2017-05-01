
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

    if(sha256_crypt.verify(password, data[0])):
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

#send user's longitude and latitude data
@app.route('/sendLoc', methods=['GET', 'POST'])
def sendLoc():
	lat = request.form['latitude']
	lon = request.form['longitude']
	cursor = conn.cursor()
	
	if('username' in session):
		username = session['username']
        cursor.execute('SELECT * FROM Location')
        print cursor.fetchall()

		query = 'SELECT * FROM Location WHERE username = %s'
		cursor.execute(query, (username,))
    
		#stores the results in a variable
		data = cursor.fetchone()
		#use fetchall() if you are expecting more than 1 data row
		if(data):
			#If the previous query returns data, then user exists already
			ins = 'UPDATE Location SET latitude = %f, longitude = %f WHERE username = %s'
			cursor.execute(ins, (lat, lon, username))
			conn.commit()
			cursor.close()
			return redirect(url_for('index'))
		else:
			#If the user doesn't exist add them
			ins = 'INSERT INTO Location VALUES(%s, %f, %f)'
			cursor.execute(ins, (username, lon, lat))
			conn.commit()
			cursor.close()
			return redirect(url_for('index'))
	else
		return redirect(url_for('index'))
	
#send user's longitude and latitude data
@app.route('/getNearbyUsers', methods=['GET', 'POST'])
def getNearbyUsers():

	cursor = conn.cursor()
	
	if('username' in session):
		username = session['username']
		query = 'SELECT * FROM Location WHERE username = %s'
		cursor.execute(query, (username,))
    
		#stores the results in a variable
		data = cursor.fetchone()
		latitude = data[1]
		longitude = data[2]
		
		#use fetchall() if you are expecting more than 1 data row
		if(data):
			#If the previous query returns data, then user exists already
			ins = 'SELECT username FROM Location WHERE ABS(latitude-%f)<0.01 and ABS(longitude-%f<)<0.01'
			cursor.execute(ins, (lat, lon))
			
			data = cursor.fetchall()
			
			cursor.close()
			
			#this should really be JSON
            # response = []
            # for row in data:


            #hopefully this works
			return data
		else:
			error = "Try reloading the app"
			cursor.close()
			return error
	else
		return redirect(url_for('index'))
	

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')

app.secret_key = 'ihaveasecret'
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9800)
