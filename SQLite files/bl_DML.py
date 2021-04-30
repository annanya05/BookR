import pandas as pd
import sqlite3

#Connect to database
conn = sqlite3.connect('booklist.sqlite')
cur = conn.cursor()

#Read csv file
df = pd.read_csv(r'C:\Users\HP\Desktop\project\code\amazon_products.csv')

for row in df.itertuples():
	cur.execute('''INSERT INTO Books_List (Title, Author, Customer_Rating, Price) VALUES (?,?,?,?)''', (row.Title, row.Author, row.Rating, row.Price,))

conn.commit()
cur.close()

print("Database created.")