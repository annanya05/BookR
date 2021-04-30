import pandas as pd
import sqlite3

#Connect to database
conn = sqlite3.connect('ratings.sqlite')
cur = conn.cursor()

#Read csv file
df = pd.read_csv(r'C:\Users\HP\Desktop\project\DATASET\bx_ratings.csv', low_memory = False)

i = 0
for row in df.itertuples():
	r = (row.Rating)/2
	cur.execute('''INSERT INTO Ratings (user_id, book_id, rating) VALUES (?,?,?)''', (row.uid, row.ISBN, r,))
	print(i)
	i += 1

conn.commit()
cur.close()

print("Database created.") 