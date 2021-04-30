#DDL for creation of User database

import sqlite3

conn = sqlite3.connect('userdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS User')
cur.execute('''CREATE TABLE User (
user_id INTEGER PRIMARY KEY,
Name TEXT,
Age INTEGER,
Sex TEXT,
Location TEXT,
username TEXT,
password TEXT)''')

print("Table created successfully.")

cur.close()