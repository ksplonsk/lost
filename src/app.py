import sys
import json
import datetime
from flask import Flask, render_template, request
from config import dbname, dbhost, dbport
import sys
import psycopg2

#conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
#cur = conn.cursor()

app = Flask(__name__)

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
		return render_template('dashboard.html', username=username)

		# if username and password dont exist, go back to login page

@app.route('/create_user', methods=('GET', 'POST'))
def create_user():
	if request.method=='GET':
		return render_template('create_user.html')

	if request.method=='POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']

		# check to see if username is in the database
		return render_template('user_already_exists.html', username=username)

		# if username doesnt exist, add username and password into the dictionary

		# return render_template('user_created.html', username=username)


@app.route('/dashboard', methods=('GET', 'POST',))
def dashboard():
	return render_template('dashboard.html')