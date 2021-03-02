import pandas as pd
import sqlite3

#Create connections with databases
conn = sqlite3.connect('authordb.sqlite')
cur = conn.cursor()

#Reading csv file
df = pd.read_csv(r'C:\Users\HP\Desktop\project\DATASET\bx_book.csv', low_memory = False)

i = 0
for row in df.itertuples():
	cur.execute('SELECT author_id FROM Author WHERE Name=?', (row.Author,))
	rec = cur.fetchone()
	if rec is None:
		cur.execute('''INSERT INTO Author (Name) VALUES (?)''', (row.Author,))
	
	print(i)
	i += 1

conn.commit()
cur.close()

print("Database created.")