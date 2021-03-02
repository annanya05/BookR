import pandas as pd
import sqlite3

#Create connections with databases
conn = sqlite3.connect('bookdb.sqlite')
cur = conn.cursor()

#Reading csv file
df = pd.read_csv(r'C:\Users\HP\Desktop\project\DATASET\bx_book.csv', low_memory = False)

i = 0
for row in df.itertuples():
	cur.execute('''INSERT INTO Book (book_id, Title, Price) VALUES (?,?,'NULL')''', (row.ISBN, row.Title,))
	print(i)
	i += 1

conn.commit()
cur.close()

print("Database created.")