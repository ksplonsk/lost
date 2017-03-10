import csv
import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur = conn.cursor()

with open('users.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, quotechar="'")
    writer.writerow(['username', 'password', 'role', 'active'])
    
    SQL = "SELECT u.username, u.password, r.title, u.active FROM users AS u INNER JOIN roles AS r ON r.role_pk=u.role_fk"
    cur.execute(SQL)
    user_results = cur.fetchall()

    for result in user_results:
    	writer.writerow([result[0], result[1], result[2], result[3]])

with open('facilities.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, quotechar="'")
    writer.writerow(['fcode', 'common_name'])
    
    SQL = "SELECT fcode, common_name FROM facilities"
    cur.execute(SQL)
    facilities_results = cur.fetchall()

    for result in facilities_results:
    	writer.writerow([result[0], result[1]])

with open('assets.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, quotechar="'")
    writer.writerow(['asset_tag', 'description', 'facility', 'acquired', 'disposed'])
    
    SQL = "SELECT a.asset_tag, a.description, f.common_name, at.arrival, at.departure FROM assets AS a INNER JOIN asset_at AS at ON a.asset_pk=at.asset_fk INNER JOIN facilities AS f ON f.facility_pk=at.facility_fk"
    cur.execute(SQL)
    asset_results = cur.fetchall()

    for result in asset_results:
    	writer.writerow([result[0], result[1], result[2], result[3], result[4]])

