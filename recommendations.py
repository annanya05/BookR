import sqlite3

conn = sqlite3.connect('recommendations.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Recommendation_List')
cur.execute('''CREATE TABLE Recommendation_List (
list_id INTEGER,
book TEXT
)''')

print("Table created successfully.")

cur.close()