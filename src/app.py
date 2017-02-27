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

		SQL = "SELECT password, role_fk FROM users WHERE username=%s;"
		cur.execute(SQL, (username,))
		user = cur.fetchone()

		# if no user by that name, go to unmatched page
		if user == None:
			return render_template('unmatched.html', username=username)

		# if username and password don't exist, go back to unmatched page
		if user[0] == password:
			session['username'] = username
			session['logged_in'] = True
			SQL = "SELECT * FROM roles WHERE role_pk=%s;"
			cur.execute(SQL, (user[1],))
			role = cur.fetchone()
			session['role'] = role[1]
			return redirect(url_for('dashboard'))

		else:
			return render_template('unmatched.html', username=username)

@app.route('/create_user', methods=('GET', 'POST'))
def create_user():
	if request.method=='GET':
		#<option value="Logistics Officer">Logistics Officer</option>
		#<option value="Facilities Officer">Facilities Officer</option>

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT title FROM roles;"
		cur.execute(SQL)
		roles = cur.fetchall()

		role_options = []
		for role in roles:
			role_options.append(role[0])
		return render_template('create_user.html', role_options=role_options)

	if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
		username = request.form['username']
		password = request.form['password']
		selected_role = request.form['role']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM users WHERE username=%s;"
		cur.execute(SQL, (username,))
		user = cur.fetchone()

		# check to see if username is in the database
		if user != None:
			return render_template('user_already_exists.html', username=username)

		# if username doesn't exist, add username and password to the database
		SQL = "INSERT INTO users (user_pk, username, password, role_fk) VALUES (DEFAULT, %s, %s, (SELECT role_pk FROM roles WHERE (title = %s)));"
		cur.execute(SQL, (username,password,selected_role))
		conn.commit()

		return render_template('user_created.html', username=username)


@app.route('/dashboard', methods=('GET',))
def dashboard():
	return render_template('dashboard.html')

@app.route('/add_facility', methods=('GET', 'POST'))
def add_facility():
	if request.method=='GET':

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM facilities;"
		cur.execute(SQL)
		all_facilities = cur.fetchall()

		facilities = []
		for facility in all_facilities:
			facilities.append("{} ({}), {}".format(facility[2], facility[1], facility[3]))
		return render_template('add_facility.html', facilities=facilities)

	if request.method=='POST' and 'common_name' in request.form and 'fcode' in request.form and 'location' in request.form:
		common_name = request.form['common_name']
		fcode = request.form['fcode']
		location = request.form['location']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM facilities WHERE (common_name=%s OR fcode=%s);"
		cur.execute(SQL, (common_name, fcode))
		facility = cur.fetchone()

		# if facility already exists, go to facility already exists page
		if facility != None:
			return render_template('facility_already_exists.html', common_name=common_name, fcode=fcode)

		SQL = "INSERT INTO facilities (facility_pk, common_name, fcode, location) VALUES (DEFAULT, %s, %s, %s);"
		cur.execute(SQL, (common_name,fcode,location))
		conn.commit()
		
		return redirect(url_for('add_facility'))

@app.route('/add_asset', methods=('GET', 'POST'))
def add_asset():
	if request.method=='GET':

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM assets;"
		cur.execute(SQL)
		all_assets = cur.fetchall()

		assets = []
		for asset in all_assets:
			assets.append("{}: {}".format(asset[1], asset[2]))

		SQL = "SELECT common_name FROM facilities;"
		cur.execute(SQL)
		all_facilities = cur.fetchall()

		facilities = []
		for facility in all_facilities:
			facilities.append(facility[0])

		return render_template('add_asset.html', assets=assets, facilities=facilities)

	if request.method=='POST' and 'common_name' in request.form and 'asset_tag' in request.form and 'description' in request.form and 'arrival' in request.form:
		common_name = request.form['common_name']
		asset_tag = request.form['asset_tag']
		description = request.form['description']
		arrival = request.form['arrival']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM assets WHERE asset_tag=%s;"
		cur.execute(SQL, (asset_tag,))
		asset = cur.fetchone()

		# if asset already exists, go to asset already exists page
		if asset != None:
			return render_template('asset_already_exists.html', asset_tag=asset_tag)

		SQL = "INSERT INTO assets (asset_pk, asset_tag, description) VALUES (DEFAULT, %s, %s);"
		cur.execute(SQL, (asset_tag,description))

		SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrival) VALUES ((SELECT asset_pk FROM assets WHERE (asset_tag = %s)), (SELECT facility_pk FROM facilities WHERE (common_name = %s)), %s);"
		cur.execute(SQL, (asset_tag,common_name,arrival))

		conn.commit()
		
		return redirect(url_for('add_asset'))


@app.route('/dispose_asset', methods=('GET', 'POST'))
def dispose_asset():
	if request.method=='GET':

		# if not session['logged_in'] or session['role'] != 'Logistics Officer':
		# 	return render_template('asset_dispose_error.html', error_reason="only Logistics Officers cannot dispose of assets.")

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM assets WHERE disposed=false;"
		cur.execute(SQL)
		all_assets = cur.fetchall()

		assets = []
		for asset in all_assets:
			assets.append("{}: {}".format(asset[1], asset[2]))

		return render_template('dispose_asset.html', assets=assets)

	if request.method=='POST' and 'asset_tag' in request.form and 'disposal_date' in request.form:
		asset_tag = request.form['asset_tag']
		disposal_date = request.form['disposal_date']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM assets WHERE asset_tag=%s;"
		cur.execute(SQL, (asset_tag,))
		asset = cur.fetchone()

		# if asset doesn't exist, cannot be disposed of
		if asset == None:
			return render_template('asset_dispose_error.html', error_reason="that asset does not exist and therfore cannot be disposed of.")

		# if asset has already been disposed of, cannot be disposed again
		if asset[3]:
			return render_template('asset_dispose_error.html', error_reason="asset has already been disposed of.")

		SQL = "UPDATE assets SET disposed=True WHERE asset_tag=%s;"
		cur.execute(SQL, (asset_tag,))

		SQL = "UPDATE asset_at SET departure=%s WHERE (departure IS NULL AND asset_fk=(SELECT asset_pk FROM assets WHERE asset_tag=%s))"
		cur.execute(SQL, (disposal_date, asset_tag))

		conn.commit()
		
		return redirect(url_for('dashboard'))

@app.route('/asset_report', methods=('GET', 'POST'))
def asset_report():
	if request.method=='GET':

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM assets;"
		cur.execute(SQL)
		all_assets = cur.fetchall()

		assets = []
		for asset in all_assets:
			assets.append("{}: {}".format(asset[1], asset[2]))

		SQL = "SELECT common_name FROM facilities;"
		cur.execute(SQL)
		all_facilities = cur.fetchall()

		facilities = ['All']
		for facility in all_facilities:
			facilities.append(facility[0])

		return render_template('add_asset.html', assets=assets, facilities=facilities)

	if request.method=='POST' and 'common_name' in request.form and 'report_date' in request.form:
		common_name = request.form['common_name']
		report_date = request.form['report_date']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT * FROM assets WHERE asset_tag=%s;"
		cur.execute(SQL, (asset_tag,))
		asset = cur.fetchone()

		# if asset already exists, go to asset already exists page
		if asset != None:
			return render_template('asset_already_exists.html', asset_tag=asset_tag)

		SQL = "INSERT INTO assets (asset_pk, asset_tag, description) VALUES (DEFAULT, %s, %s);"
		cur.execute(SQL, (asset_tag,description))

		SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrival) VALUES ((SELECT asset_pk FROM assets WHERE (asset_tag = %s)), (SELECT facility_pk FROM facilities WHERE (common_name = %s)), %s);"
		cur.execute(SQL, (asset_tag,common_name,arrival))

		conn.commit()
		
		return redirect(url_for('add_asset'))


