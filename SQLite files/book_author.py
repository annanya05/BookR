#DDL for creation of Book_Author database

import sqlite3

conn = sqlite3.connect('book_authordb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Book_Author')
cur.execute('''CREATE TABLE Book_Author (
book_id TEXT,
author_id INTEGER,
FOREIGN KEY (book_id) REFERENCES Book(book_id),
FOREIGN KEY (author_id) REFERENCES Author(author_id))''')

print("Table created successfully.")

cur.close()