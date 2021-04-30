import pandas as pd
import sqlite3

#Create connections with databases

connB = sqlite3.connect('bookdb.sqlite')
curB = connB.cursor()


connA = sqlite3.connect('authordb.sqlite')
curA = connA.cursor()


connBA = sqlite3.connect('book_authordb.sqlite')
curBA = connBA.cursor()

#Reading csv file
df = pd.read_csv(r'C:\Users\HP\Desktop\project\DATASET\bx_book.csv', low_memory = False)

i = 0
for row in df.itertuples():
	curB.execute('SELECT book_id FROM Book WHERE Title=?', (row.Title,))
	rec1 = curB.fetchone()
	bid = rec1[0]

	curA.execute('SELECT author_id FROM Author WHERE Name=?', (row.Author,))
	rec2 = curA.fetchone()
	aid = rec2[0]
	
	curBA.execute('''INSERT INTO Book_Author (book_id, author_id) VALUES (?,?)''', (bid, aid,))

	print(i)
	i += 1

connBA.commit()

curB.close()
curA.close()
curBA.close()

print("Database created.")
	