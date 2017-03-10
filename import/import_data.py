import csv
import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur = conn.cursor()
#TODO: make sure argv[2] has a / on the end

with open(sys.argv[2]+'users.csv') as csvfile:
	rows = csv.DictReader(csvfile)

	for row in rows:
		cur.execute("INSERT INTO users (role_fk, username, password, active) VALUES ((SELECT role_pk FROM roles WHERE title=%s), %s, %s, %s)", (row['role'], row['username'], row['password'], row['active']))
	
	conn.commit()

with open(sys.argv[2]+'facilities.csv') as csvfile:
	rows = csv.DictReader(csvfile)

	for row in rows:
		cur.execute("INSERT INTO facilities (fcode, common_name) VALUES (%s, %s)", (row['fcode'], row['common_name']))
	
	conn.commit()

with open(sys.argv[2]+'assets.csv') as csvfile:
	rows = csv.DictReader(csvfile)

	for row in rows:
		disposed = 't'
		if row['disposed'] == 'NULL':
			disposed = 'f'
		cur.execute("INSERT INTO assets (asset_tag, description, disposed) VALUES (%s, %s, %s)", (row['asset_tag'], row['description'], disposed))
		
		departure = row['disposed']
		if departure == 'NULL':
			departure = None
		cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrival, departure) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag=%s), (SELECT facility_pk FROM facilities WHERE fcode=%s), %s, %s)", (row['asset_tag'], row['facility'], row['acquired'], departure))
	
	conn.commit()

with open(sys.argv[2]+'transfers.csv') as csvfile:
	rows = csv.DictReader(csvfile)

	for row in rows:

		approve_dt = row['approve_dt']
		if approve_dt == '':
			approve_dt = None

		SQL = """INSERT INTO transfers (requester_fk, request_dt, source_fk, destination_fk, asset_fk, approver_fk, approved_dt) VALUES (
			(SELECT user_pk FROM users WHERE username=%s),
			%s,
			(SELECT facility_pk FROM facilities WHERE fcode=%s),
			(SELECT facility_pk FROM facilities WHERE fcode=%s),
			(SELECT asset_pk FROM assets WHERE asset_tag=%s),
			(SELECT user_pk FROM users WHERE username=%s),
			%s
			) """
		cur.execute(SQL, (row['request_by'], row['request_dt'], row['source'], row['destination'], row['asset_tag'], row['approve_by'], approve_dt))
		
		cur.execute("SELECT transfer_pk FROM transfers")
		transfers = cur.fetchall()
		transfer_fk = transfers[-1][0]

		load_dt = row['load_dt']
		if load_dt == 'NULL':
			load_dt = None

		unload_dt = row['unload_dt']
		if unload_dt == 'NULL':
			unload_dt = None

		cur.execute("INSERT INTO in_transit (transfer_fk, load_dt, unload_dt) VALUES (%s, %s, %s)", (transfer_fk, load_dt, unload_dt))
	conn.commit()



