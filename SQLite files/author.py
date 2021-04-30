#DDL for creation of Author database

import sqlite3

conn = sqlite3.connect('authordb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Author')
cur.execute('''CREATE TABLE Author (
author_id INTEGER PRIMARY KEY,
Name TEXT)''')

print("Table created successfully.")

cur.close()