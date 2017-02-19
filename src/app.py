import sys
import json
import datetime
from flask import Flask, render_template, request
# from config import dbname, dbhost, dbport
import sys
import psycopg2

app = Flask(__name__)

dbname = 'lost'
dbhost = '127.0.0.1'
dbport = 5432
conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
cur = conn.cursor()

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
	if request.method=='GET':
		return render_template('login.html')

	if request.method=='POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']

		# check to see if username is in the database
		#return render_template('dashboard.html', username=username)

		# if username and password dont exist, go back to login page
		return render_template('unmatched.html', username=username)

@app.route('/create_user', methods=('GET', 'POST'))
def create_user():
	if request.method=='GET':
		return render_template('create_user.html')

	if request.method=='POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']

		SQL = "SELECT * FROM users WHERE username=%s;"
 		data = (name,)
		cur.execute(SQL, data)
		user_res = cur.fetchall()

		# check to see if username is in the database
		return render_template('user_already_exists.html', username=username)

		# if username doesnt exist, add username and password into the dictionary

		# return render_template('user_created.html', username=username)


@app.route('/dashboard', methods=('GET',))
def dashboard():
	return render_template('dashboard.html')