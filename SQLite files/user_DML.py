import pandas as pd
import sqlite3

#Create connection with database
conn = sqlite3.connect('userdb.sqlite')
cur = conn.cursor()

#Reading csv file
df = pd.read_csv('bx_user.csv', low_memory = False)

for row in df.itertuples():
	cur.execute('''INSERT INTO User (Name, Age, Sex, Location, username, password) VALUES ('NULL',?,'NULL',?,'NULL','NULL')''', (row.Age, row.Location, ))

conn.commit()
cur.close()

print("Database created.")