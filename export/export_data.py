import csv
import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur = conn.cursor()

# make sure argv[2] has a / on the end
dir = sys.argv[2]
if dir != '' and not dir.endswith('/'):
    dir = dir + '/'

# export users
with open(dir+'users.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, quotechar="'")
	writer.writerow(['username', 'password', 'role', 'active'])
    
	SQL = "SELECT u.username, u.password, r.title, u.active FROM users AS u INNER JOIN roles AS r ON r.role_pk=u.role_fk"
	cur.execute(SQL)
	user_results = cur.fetchall()

	for result in user_results:
		writer.writerow([result[0], result[1], result[2], result[3]])

# export facilities
with open(dir+'facilities.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, quotechar="'")
	writer.writerow(['fcode', 'common_name'])
    
	SQL = "SELECT fcode, common_name FROM facilities"
	cur.execute(SQL)
	facilities_results = cur.fetchall()

	for result in facilities_results:
		writer.writerow([result[0], result[1]])

# export assets
with open(dir+'assets.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, quotechar="'")
	writer.writerow(['asset_tag', 'description', 'facility', 'acquired', 'disposed'])
    
	SQL = "SELECT a.asset_tag, a.description, f.fcode, at.arrival, at.departure FROM assets AS a INNER JOIN asset_at AS at ON a.asset_pk=at.asset_fk INNER JOIN facilities AS f ON f.facility_pk=at.facility_fk"
	cur.execute(SQL)
	asset_results = cur.fetchall()

	for result in asset_results:
		r4 = result[4]
		if result[4] == None:
			r4 = 'NULL'

		writer.writerow([result[0], result[1], result[2], result[3], r4])

# expirt transfers
with open(dir+'transfers.csv', 'w') as csvfile:
	writer = csv.writer(csvfile, quotechar="'")
	writer.writerow(['asset_tag', 'request_by', 'request_dt', 'approve_by', 'approve_dt', 'source', 'destination', 'load_dt', 'unload_dt'])
    
	SQL = "SELECT a.asset_tag, u1.username, t.request_dt, u2.username, t.approved_dt, f1.fcode, f2.fcode, it.load_dt, it.unload_dt FROM transfers AS t INNER JOIN users AS u1 ON t.requester_fk=u1.user_pk INNER JOIN users AS u2 ON t.approver_fk=u2.user_pk INNER JOIN assets AS a ON t.asset_fk=a.asset_pk INNER JOIN facilities AS f1 ON t.source_fk=f1.facility_pk INNER JOIN facilities AS f2 ON t.destination_fk=f2.facility_pk INNER JOIN in_transit AS it ON it.transfer_fk=t.transfer_pk"
	cur.execute(SQL)
	transfer_results = cur.fetchall()

	for result in transfer_results:
		r7 = result[7]
		r8 = result[8]
		if result[7] == None:
			r7 = 'NULL'
		if result[8] == None:
			r8 = 'NULL'

		writer.writerow([result[0], result[1], result[2], result[3], result[4], result[5], result[6], r7, r8])

