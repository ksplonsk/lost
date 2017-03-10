import csv
import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur = conn.cursor()

with open(sys.argv[2]+'facilities.csv') as csvfile:
	rows = csv.DictReader(csvfile)
	for row in rows:
		cur.execute("INSERT INTO facilities (fcode, common_name) VALUES (%s, %s)", (row['fcode'], row['common_name']))
	conn.commit()