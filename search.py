import merge
import sqlite3

conn = sqlite3.connect('recommendations (1).sqlite')
cur = conn.cursor()

bname = "Meg"
rlist = []
rlist = merge.result(bname=bname)
print(rlist)

uid = 278862

for i in rlist:
    cur.execute('''INSERT INTO Recommendation_List (list_id, book) VALUES (?, ?)''', (uid, i,))

conn.commit()
cur.close()