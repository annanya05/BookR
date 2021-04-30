#DDL for creation of Books_List database

import sqlite3

conn = sqlite3.connect('booklist.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Books_List')
cur.execute('''CREATE TABLE Books_List (
books_id INTEGER PRIMARY KEY,
Title TEXT,
Author TEXT,
Customer_Rating REAL,
Price REAL)''')

print("Table created successfully.")

cur.close()