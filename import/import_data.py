import csv
import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur = conn.cursor()

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
		SQL = """ """
		cur.execute("INSERT INTO transfers (request_dt, approved_dt) VALUES (%s, %s)", (row['request_dt'], row['approve_dt']))
		#cur.execute("INSERT INTO in_transit (facility_fk, arrival, departure) VALUES ((SELECT facility_pk FROM facilities WHERE fcode=%s), %s, %s)", (row['facility'], row['aquired'], row['disposed']))
	conn.commit()



