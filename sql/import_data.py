import csv
import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()

with open('osnap_legacy/product_list.csv') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cur.execute("INSERT INTO products (vendor, description, alt_description) VALUES (%s, %s, %s)", (row[4], row[0], row[2]))

with open('osnap_legacy/DC_inventory.csv') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cur.execute("INSERT INTO products (description) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM products WHERE (description = %s AND vendor IS NULL))", (row[1],row[1]))
        cur.execute("INSERT INTO assets (product_fk, asset_tag) VALUES ((SELECT product_pk FROM products WHERE (description = %s AND vendor IS NULL) LIMIT 1),%s)", (row[1],row[0]))

with open('osnap_legacy/HQ_inventory.csv') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cur.execute("INSERT INTO products (description) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM products WHERE (description = %s AND vendor IS NULL))", (row[1],row[1]))
        cur.execute("INSERT INTO assets (product_fk, asset_tag) VALUES ((SELECT product_pk FROM products WHERE (description = %s AND vendor IS NULL) LIMIT 1),%s)", (row[1],row[0]))

with open('osnap_legacy/MB005_inventory.csv') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cur.execute("INSERT INTO products (description) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM products WHERE (description = %s AND vendor IS NULL))", (row[1],row[1]))
        cur.execute("INSERT INTO assets (product_fk, asset_tag) VALUES ((SELECT product_pk FROM products WHERE (description = %s AND vendor IS NULL) LIMIT 1),%s)", (row[1],row[0]))

with open('osnap_legacy/NC_inventory.csv') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cur.execute("INSERT INTO products (description) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM products WHERE (description = %s AND vendor IS NULL))", (row[1],row[1]))
        cur.execute("INSERT INTO assets (product_fk, asset_tag) VALUES ((SELECT product_pk FROM products WHERE (description = %s AND vendor IS NULL) LIMIT 1),%s)", (row[1],row[0]))

with open('osnap_legacy/SPNV_inventory.csv') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cur.execute("INSERT INTO products (description) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM products WHERE (description = %s AND vendor IS NULL))", (row[1],row[1]))
        cur.execute("INSERT INTO assets (product_fk, asset_tag) VALUES ((SELECT product_pk FROM products WHERE (description = %s AND vendor IS NULL) LIMIT 1),%s)", (row[1],row[0]))

with open('osnap_legacy/transit.csv') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        cur.execute("INSERT INTO facilities (common_name) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM facilities WHERE common_name = %s)", (row[1],row[1]))
        cur.execute("INSERT INTO facilities (common_name) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM facilities WHERE common_name = %s)", (row[2],row[2]))

conn.commit()

cur.close()
conn.close()