This directory allows you to create the LOST database and migrate the legacy data

Files:
README.txt - this readme file
create_tables.sql - sql script that generates base tables
import_data.py - python script to generate and import data
import_data.sh - bash script to import data, run python script and cleanup at the end

Note: to run import_data.sh and import_data.py you must cd into your sql directory