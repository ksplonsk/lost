from flask import Flask, render_template, request
# from config import dbname, dbhost, dbport
# import sys
# import psycopg2

# conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
# cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/report_menu')
def report_menu():
	# cur.execute("SELECT * FROM assets")
	# records = cur.fetchall()
	# processed_data = []
	# for r in res:
	# 	processed_data.append( dict(zip(('asset_tag', 'description'), r)))
	# return render_template('report_menu.html', processed_data=processed_data)
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


@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
	# Try to handle as plaintext
	if request.method=='POST' and 'arguments' in request.form:
		req=json.loads(request.form['arguments'])

	dat = dict()
	dat['timestamp'] = req['timestamp']
	dat['result'] = 'OK'
	data = json.dumps(dat)
	return data


@app.route('/rest/test', methods=('POST',))
def test():
	# Try to handle as plaintext

	dat = dict()
	dat['timestamp'] = '2017-02-11'
	dat['result'] = 'OK'
	data = json.dumps(dat)
	return data


# if __name__ == "__main__":
# 	app.run(host='0.0.0.0',port=8080)
