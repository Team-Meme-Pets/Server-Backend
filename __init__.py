
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import hashlib

import psycopg2

from passlib.hash import sha256_crypt
import datetime

app = Flask(__name__)
Session(app)

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
	
	print("user: %s    password: %s",username,password)
	
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT password FROM UserAccount WHERE username = %s'
	cursor.execute(query, (username,))
	
	#stores the results in a variable
	data = cursor.fetchone()
	if(not data):
		error = 'Invalid login or username'
		print("invalid username: %s", username)
		return error
	
	cursor.close()
	error = None

	if(sha256_crypt.verify(password, data[0])):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['logged_in'] = True
		print("Login Success: %s", username)
		return "Success"
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		print("invalid login: %s", username)
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
		print("This username exists already: %s", username)
		return error
	else:
		ins = 'INSERT INTO UserAccount VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password2, email, timestamp, timestamp))
		conn.commit()
		cursor.close()
		print("Reg Success: %s", username)
		return "Welcome"

#send user's longitude and latitude data
@app.route('/sendLoc', methods=['GET', 'POST'])
def sendLoc():
	lat = request.form['latitude']
	lon = request.form['longitude']
	cursor = conn.cursor()

	#cursor.execute('SELECT * FROM UserAccount')
	#data = cursor.fetchall()
	#print data
	
	if('username' in session):
		username = session['username']
		cursor.execute('SELECT * FROM Location')
		print cursor.fetchall()
		print "is this even working"

		query = 'SELECT * FROM Location WHERE username = %s'
		cursor.execute(query, (username,))

		#stores the results in a variable
		data = cursor.fetchone()
		#use fetchall() if you are expecting more than 1 data row
		if(data):
			#If the previous query returns data, then user exists already
			ins = 'UPDATE Location SET latitude = %s, longitude = %s WHERE username = %s'
			cursor.execute(ins, (lat, lon, username))
			conn.commit()
			cursor.close()
			return "Success"
		else:
			#If the user doesn't exist add them
			ins = 'INSERT INTO Location VALUES(%s, %s, %s)'
			cursor.execute(ins, (username, lon, lat))
			conn.commit()
			cursor.close()
			return "Success"
	else:
		return redirect(url_for('index'))
	
#gets users within 0.05 lat and lon
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
			ins = 'SELECT * FROM Location WHERE ABS(latitude-%s)<0.05 and ABS(longitude-%s)<0.05'
			cursor.execute(ins, (latitude, longitude))
			
			data = cursor.fetchall()
			#print data
			
			cursor.close()

			response = []
			for row in data:
				t = {'username': row[0], 'latitude': float(row[1]), 'longitude': float(row[2])}
				#print row[1]
				response.append(t)

			return jsonify(response)
		else:
			error = "Try reloading the app"
			cursor.close()
			return error
	else:
		return redirect(url_for('index'))

#Add ownership of a pet to user
@app.route('/addPet', methods=['GET', 'POST'])
def addPet():
	pet_name = request.form['pet_name']
	
	cursor = conn.cursor()
	
	if('username' in session):
		username = session['username']
		query = 'SELECT * FROM HavePet WHERE username = %s and pet_name = %s'
		cursor.execute(query, (username, pet_name))

		#stores the results in a variable
		data = cursor.fetchone()
		#use fetchall() if you are expecting more than 1 data row
		if(data):
			error = "You already have this pet"
			cursor.close()
			return error
		else:
			ins = 'INSERT INTO HavePet VALUES(%s, %s)'
			cursor.execute(ins, (username, pet_name))
			conn.commit()
			cursor.close()
			return "Success"
	else:
		return redirect(url_for('index'))

#get user's pets
@app.route('/viewPets', methods=['GET', 'POST'])
def viewPets():

	cursor = conn.cursor()
	
	if('username' in session):
		username = session['username']
		query = 'SELECT * FROM HavePet WHERE username = %s'
		cursor.execute(query, (username,))
	
		#stores the results in a variable
		data = cursor.fetchall()
		
		#use fetchall() if you are expecting more than 1 data row
		if(data):
			cursor.close()

			response = []
			for row in data:
				t = {'username': row[0], 'pet_name': row[1]}
				response.append(t)

			return jsonify(response)
		else:
			error = "Try reloading the app"
			cursor.close()
			return error
	else:
		return redirect(url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session.pop('username', None)
	print("Logout Success")
	return "Success"

if __name__ == "__main__":
	app.secret_key = 'ihaveasecret'
	app.run(host='0.0.0.0',port=9800)