import sys
import json
import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from config import dbname, dbhost, dbport
import sys
import psycopg2

app = Flask(__name__)

app.config["SECRET_KEY"] = 'development_key'

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

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM users WHERE username=%s;"
		cur.execute(SQL, (username,))
		user = cur.fetchone()

		# if no user by that name, go to unmatched page
		if user == None:
			return render_template('unmatched.html', username=username)

		# if username and password don't exist, go back to unmatched page
		if user[2] == password:
			session['username'] = username
			session['logged_in'] = True
			return redirect(url_for('dashboard'))

		else:
			return render_template('unmatched.html', username=username)

@app.route('/create_user', methods=('GET', 'POST'))
def create_user():
	if request.method=='GET':
		return render_template('create_user.html')

	if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
		username = request.form['username']
		password = request.form['password']
		role = request.form['role']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM users WHERE username=%s;"
		cur.execute(SQL, (username,))
		user = cur.fetchone()

		# check to see if username is in the database
		if user != None:
			return render_template('user_already_exists.html', username=username)

		# if username doesn't exist, add username and password to the database
		SQL = "INSERT INTO users (user_pk, username, password, roles_fk) VALUES (DEFAULT, %s, %s, (SELECT role_pk FROM roles WHERE (title = %s)));"
		cur.execute(SQL, (username,password))
		conn.commit()

		return render_template('user_created.html', username=username)


@app.route('/dashboard', methods=('GET',))
def dashboard():
	return render_template('dashboard.html')
