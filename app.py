
"""
Created on Thu Dec 14 16:12:43 2017

@author: Arjun
"""

#imports
from flask import Flask, render_template, json, request, session, redirect
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.mysql import MySQL

#initialize the flask and SQL Objects
app = Flask(__name__)
mysql = MySQL()

#initializa secret key
app.secret_key='This is my secret key'

#configure MYSQL
app.config['MYSQL_DATABASE_USER'] = 'Arjun'
app.config['MYSQL_DATABASE_PASSWORD'] = '1377Hello!'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#helper function
def check_password(acc_pass, provided_pass):
	#provided_pass = generate_password_hash(provided_pass)
	if provided_pass==acc_pass:
		return True
	return False

#define methods for routes (what to do and display)
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/main")
def return_main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/showSignIn')
def showSignIn():
	return render_template('signin.html')

@app.route('/wishlist')
def wishlist():
	return render_template('wishlist.html')

@app.route('/userHome')
def showUserHome():
	#check that someone has logged in correctly
	if session.get("user"):
		return render_template('userHome.html', username=session.get("user")[1])
	else:
		return render_template('error.html', error = "Invalid User Credentials")

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect('/')

@app.route('/validateLogin', methods=['POST'])
def validate():
	try:
		_username = request.form['inputEmail']
		_password = request.form['inputPassword']
		print("Username:", _username, "\n Password:", _password)

		#create MySQL Connection
		conn = mysql.connect()
		#create a cursor to query the stored procedure
		cursor = conn.cursor()
		print("successfully connected to mysql!")

		#get users with this username (should only be one)
		cursor.callproc('sp_validateLogin', (_username,))
		users = cursor.fetchall()
		print("called process")
		#acctually validate these users
		if len(users)>0:
			if check_password(users[0][3], _password):
				session['user']=users[0]
				return redirect('/userHome')
			else:
				return render_template('error.html', error="incorrect username or password")
		else:
			return render_template('error.html', error= "incorrect username or password")

	except Exception as ex:
		print("Error getting username and password, Error:", ex)
		return render_template('error.html', error = 'Missing Email Adress or Password')

	finally:
		#disconnect from mysql database
		cursor.close()
		conn.close()

@app.route('/signUp', methods=['POST'])
def signUp():
	"""
	method to deal with creating a new user in the MySQL Database
	"""
	print("signing up user...")
	try:
		#read in values from frontend
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']

		#Make sure we got all the values
		if _name and _email and _password:
			print("Email:", _email, "\n", "Name:", _name, "\n", "Password:", _password)
	
			#create MySQL Connection
			conn = mysql.connect()
			#create a cursor to query the stored procedure
			cursor = conn.cursor()

			#has passowrd for security
			_hashed_password = generate_password_hash(_password)
			print("Hashed Password:", _hashed_password)

			#call jQuery to make a POST request to the DB with the info
			cursor.callproc('sp_createUser', (_name, _email, _password))
			print("Successfully called sp_createUser")
			#check if the POST request was successful
			data = cursor.fetchall()

			if len(data)==0:
				conn.commit()
				print('signup successful!')
				return json.dumps({'message':'User created successfuly!'})
			else:
				print('error')
				return json.dumps({'error':str(data[0])})

		else:
			print('fields not submitted')
			return json.dumps({'html' : '<span>Enter the required fields</span>'})

	except Exception as ex:
		print('got an exception: ', ex)
		return json.dumps({'error':str(ex)})

	finally:
		print('ending...')
		cursor.close()
		conn.close()



if __name__ == "__main__":
    app.run()
