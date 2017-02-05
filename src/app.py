from flask import Flask, render_template, request
from config import dbname, dbhost, dbport
import sys
import psycopg2

conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/goodbye')
def goodbye():
	if request.method=='GET' and 'mytext' in request.args:
		return render_template('goodbye.html',data=request.args.get('mytext'))

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/report_menu')
def report_menu():
	return render_template('report_menu.html')

@app.route('/facility_inventory_report')
def facility_inventory_report():
	return render_template('facility_inventory_report.html',facility=request.args.get('facility'),date=request.args.get('report_date'))

@app.route('/in_transit_report')
def in_transit_report():
	return render_template('in_transit_report.html',date=request.args.get('report_date'))

@app.route('/logout')
def logout():
	return render_template('logout.html')


	# request.form is only populated for POST messages
	if request.method=='POST' and 'mytext' in request.form:
		return render_template('goodbye.html',data=request.form['mytext'])
	return render_template('index.html')
