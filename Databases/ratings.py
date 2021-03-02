#DDL for creation of Ratings database

import sqlite3

conn = sqlite3.connect('ratings.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Ratings')
cur.execute('''CREATE TABLE Ratings (
rating_id INTEGER PRIMARY KEY,
user_id INTEGER,
book_id INTEGER,
rating REAL)''')

print("Table created successfully.")

cur.close()