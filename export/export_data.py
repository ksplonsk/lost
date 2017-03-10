import csv
import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1',port=5432)
cur = conn.cursor()

with open('users.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['username','password', 'role', 'active'])
    
    SQL = "SELECT u.username, u.password, r.title, u.active FROM users AS u INNER JOIN roles AS r ON r.role_pk=u.role_fk"
    cur.execute(SQL)
    user_results = cur.fetchall()

    for result in user_results:
    	writer.writerow([result[0], result[1], result[2], result[3]])