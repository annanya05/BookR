#DDL for creation of User_Recommendation database

import sqlite3

conn = sqlite3.connect('user_recommendation.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS User_Recommendation')
cur.execute('''CREATE TABLE User_Recommendation (
user_id INTEGER,
list_id INTEGER)''')

print("Table created successfully.")

cur.close()