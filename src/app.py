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
	conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
	cur = conn.cursor()

	SQL = "SELECT t.transfer_pk, a.asset_tag, sf.common_name, df.common_name FROM transfers AS t INNER JOIN facilities AS sf ON sf.facility_pk=t.source_fk INNER JOIN facilities AS df ON df.facility_pk=t.destination_fk INNER JOIN assets AS a ON a.asset_pk=t.asset_fk WHERE t.approver_fk IS NULL"
	cur.execute(SQL)

	approval_results = cur.fetchall()

	# build up request row dictionaries
	requests = []
	for result in approval_results:
		row = dict()
		row['transfer_pk'] = result[0]
		row['asset_tag'] = result[1]
		row['source_facility'] = result[2]
		row['destination_facility'] = result[3]
		requests.append(row)

	session['requests'] = requests

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

		# build up list of all assets
		SQL = "SELECT * FROM assets;"
		cur.execute(SQL)
		all_assets = cur.fetchall()

		assets = []
		for asset in all_assets:
			assets.append("{}: {}".format(asset[1], asset[2]))

		# build up list of all facilities
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

		# add asset to assets table
		SQL = "INSERT INTO assets (asset_pk, asset_tag, description) VALUES (DEFAULT, %s, %s);"
		cur.execute(SQL, (asset_tag,description))

		# add asset to asset_at table and associates it with a facility
		SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrival) VALUES ((SELECT asset_pk FROM assets WHERE (asset_tag = %s)), (SELECT facility_pk FROM facilities WHERE (common_name = %s)), %s);"
		cur.execute(SQL, (asset_tag,common_name,arrival))

		conn.commit()
		
		return redirect(url_for('add_asset'))


@app.route('/dispose_asset', methods=('GET', 'POST'))
def dispose_asset():
	if request.method=='GET':

		if not session['logged_in'] or session['role'] != 'Logistics Officer':
			return render_template('asset_dispose_error.html', error_reason="only Logistics Officers cannot dispose of assets.")

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

		# sets asset flag disposed to true
		SQL = "UPDATE assets SET disposed=True WHERE asset_tag=%s;"
		cur.execute(SQL, (asset_tag,))

		# set departure date to disposal date
		SQL = "UPDATE asset_at SET departure=%s WHERE (departure IS NULL AND asset_fk=(SELECT asset_pk FROM assets WHERE asset_tag=%s))"
		cur.execute(SQL, (disposal_date, asset_tag))

		conn.commit()
		
		return redirect(url_for('dashboard'))

@app.route('/asset_report', methods=('GET', 'POST'))
def asset_report():
	if request.method=='GET':

		session['asset_report'] = []

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		SQL = "SELECT common_name FROM facilities;"
		cur.execute(SQL)
		all_facilities = cur.fetchall()

		facilities = ['All']
		for facility in all_facilities:
			facilities.append(facility[0])

		return render_template('asset_report.html', facilities=facilities)

	if request.method=='POST' and 'common_name' in request.form and 'report_date' in request.form:
		common_name = request.form['common_name']
		report_date = request.form['report_date']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		# use a JOIN to get records for all facilities for the date we are concerned with
		if common_name == 'All':
			cur.execute("SELECT a.asset_tag, a.description, f.common_name, at.arrival, at.departure FROM assets AS a INNER JOIN asset_at AS at ON a.asset_pk=at.asset_fk INNER JOIN facilities AS f ON f.facility_pk=at.facility_fk WHERE at.arrival<=%s AND (at.departure IS NULL OR at.departure>=%s);", (report_date,report_date))

		# use a JOIN to get records for facility and date we are concerned with
		else:
			cur.execute("SELECT a.asset_tag, a.description, f.common_name, at.arrival, at.departure FROM assets AS a INNER JOIN asset_at AS at ON a.asset_pk=at.asset_fk INNER JOIN facilities AS f ON f.facility_pk=at.facility_fk WHERE at.arrival<=%s AND (at.departure IS NULL OR at.departure>=%s) AND f.common_name=%s;", (report_date,report_date,common_name))

		report_results = cur.fetchall()

		# build up report row dictionaries
		report = []
		for result in report_results:
			row = dict()
			row['asset_tag'] = result[0]
			row['description'] = result[1]
			row['facility'] = result[2]
			row['arrival'] = result[3]
			row['departure'] = result[4]
			report.append(row)

		session['asset_report'] = report

		SQL = "SELECT common_name FROM facilities;"
		cur.execute(SQL)
		all_facilities = cur.fetchall()

		facilities = ['All']
		for facility in all_facilities:
			facilities.append(facility[0])
		
		return render_template('asset_report.html', facilities=facilities)

@app.route('/transfer_report', methods=('GET', 'POST'))
def transfer_report():
	return render_template('transfer_report.html')

@app.route('/transfer_req', methods=('GET', 'POST'))
def transfer_req():
	if request.method=='GET':
		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		# build up list of all assets
		SQL = "SELECT asset_tag FROM assets WHERE disposed=false;"
		cur.execute(SQL)
		all_assets = cur.fetchall()

		assets = []
		for asset in all_assets:
			assets.append(asset[0])

		# build up list of all facilities
		SQL = "SELECT common_name FROM facilities;"
		cur.execute(SQL)
		all_facilities = cur.fetchall()

		facilities = []
		for facility in all_facilities:
			facilities.append(facility[0])

		return render_template('transfer_req.html', assets=assets, facilities=facilities)

	if request.method=='POST' and 'asset' in request.form and 'destination_facility' in request.form:
		asset = request.form['asset']
		destination_facility = request.form['destination_facility']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		cur.execute("SELECT user_pk FROM users WHERE (username = %s)", (session['username'],))
		requester_fk = cur.fetchone()

		cur.execute("SELECT asset_pk FROM assets WHERE (asset_tag = %s)", (asset,))
		asset_fk = cur.fetchone()

		cur.execute("SELECT facility_fk FROM asset_at WHERE (asset_fk = %s)", (asset_fk,))
		source_facility = cur.fetchone()

		cur.execute("SELECT facility_pk FROM facilities WHERE (common_name = %s)", (destination_facility,))
		destination = cur.fetchone()


		# add transfer request into DB
		SQL = "INSERT INTO transfers (transfer_pk, requester_fk, request_dt, source_fk, destination_fk, asset_fk) VALUES (DEFAULT, %s, CURRENT_TIMESTAMP, %s, %s, %s);"
		cur.execute(SQL, (requester_fk,source_facility,destination,asset_fk))
		conn.commit()

		return redirect(url_for('transfer_req_success'))



@app.route('/approve_req', methods=('GET', 'POST'))
def approve_req():

	if session['role'] != 'Facilities Officer':
		return redirect(url_for('req_approve_error'))

	if request.method=='GET':
		if not 'transfer_pk' in request.args or not 'approval_tag' in request.args:
			return # TODO: make an error

		transfer_pk = request.args['transfer_pk']
		approval_tag = request.args['approval_tag']
		return render_template('approve_req.html', transfer_pk=transfer_pk, approval_tag=approval_tag)

	if request.method=='POST' and ('approve' in request.form or 'reject' in request.form) and 'transfer_pk' in request.form:
		transfer_pk = request.form['transfer_pk']

		conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
		cur = conn.cursor()

		if request.form.get('approve'):
			SQL = "UPDATE transfers SET approver_fk=(SELECT user_pk FROM users WHERE username=%s), approved_dt=CURRENT_TIMESTAMP WHERE (transfer_pk=CAST(%s as integer))"
			cur.execute(SQL, (session['username'], transfer_pk))

			SQL = "INSERT INTO in_transit (transfer_fk, load_dt, unload_dt) VALUES (%s, NULL, NULL)"
			cur.execute(SQL, (transfer_pk,))
			conn.commit()

		if request.form.get('reject'):
			SQL = "DELETE FROM transfers WHERE (transfer_pk=CAST(%s as integer))"
			cur.execute(SQL, (transfer_pk,))
			conn.commit()
		
		return redirect(url_for('dashboard'))


@app.route('/update_transit', methods=('GET', 'POST'))
def update_transit():
	return render_template('update_transit.html')

@app.route('/logout', methods=('GET', 'POST'))
def logout():

	if request.method=='GET':
		return render_template('logout.html')

	if request.method=='POST':
		session['username'] = ''
		session['logged_in'] = False
		session['role'] = ''
		return redirect(url_for('login'))

@app.route('/transfer_req_success')
def transfer_req_success():
	return render_template('transfer_req_success.html')

@app.route('/req_approve_error', methods=('GET', 'POST'))
def req_approve_error():
	return render_template('req_approve_error.html')


