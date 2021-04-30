#DDL for creation of Recommendation_List database

import sqlite3

conn = sqlite3.connect('recommendations.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Recommendation_List')
cur.execute('''CREATE TABLE Recommendation_List (
list_id INTEGER PRIMARY KEY,
book_id INTEGER,
Score REAL)''')

print("Table created successfully.")

cur.close()