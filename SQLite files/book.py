#DDL for creation of Book database

import sqlite3

conn = sqlite3.connect('bookdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Book')
cur.execute('''CREATE TABLE Book (
book_id TEXT PRIMARY KEY,
Title TEXT NOT NULL,
Price REAL)''')

print("Table created successfully.")

cur.close()
