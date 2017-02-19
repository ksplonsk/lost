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

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/create_user')
def create_user():
	if request.method=='GET':
		return render_template('create_user.html')

	if request.method=='POST' and 'arguments' in request.form:
		req=json.loads(request.form['arguments'])
		username = req['username']
		password = req['password']

		# check to see if username is in the database

		# if username doesnt exist, add username and password into the dictionary

		return render_template('user_created.html', username=username)


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')