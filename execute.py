import sqlite3

conn = sqlite3.connect("price.db")

cur = conn.cursor()

cur.execute("UPDATE user_data SET money = ? WHERE id = ?",(321321, 132132))

conn.commit()

conn.close()