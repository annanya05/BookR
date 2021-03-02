#DDL for creation of Administrator database

import sqlite3

conn = sqlite3.connect('admindb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Administrator')
cur.execute('''CREATE TABLE Administrator (
AID INTEGER PRIMARY KEY,
Name TEXT,
admin_id TEXT NOT NULL,
password TEXT NOT NULL)''')

print("Table created successfully.")

cur.close()