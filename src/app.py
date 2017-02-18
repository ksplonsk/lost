import sys
import json
import datetime
from flask import Flask, render_template, request
from config import dbname, dbhost, dbport
import sys
import psycopg2

conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/create_user')
def login():
	return render_template('create_user.html')

@app.route('/dashboard')
def login():
	return render_template('dashboard.html')