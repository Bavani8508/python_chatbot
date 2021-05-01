import sqlite3
conn=sqlite3.connect("chatbot.db")
cursor=conn.cursor()
sql="select * from faculty2"
cursor.execute(sql)
print(cursor.fetchall())