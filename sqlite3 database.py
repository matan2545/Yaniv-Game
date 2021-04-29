import sqlite3

#connection = sqlite3.connect('yaniv.db')
#cursor = connection.cursor()

#cursor.execute("""CREATE TABLE yaniv (
 #                conn text,
  #               deck text,
   #              score integer,
    #             ind integer
     #            )""")

connection = sqlite3.connect('users.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE users (
                 username text,
                 password text,
                 score int
                 )""")

# cursor.execute("INSERT INTO decks VALUES ('127.0.0.1', '1D,2D,3D', 10)")
# cursor.execute("SELECT * FROM decks WHERE conn = '127.0.0.1'")
# print(cursor.fetchall())

connection.commit()

connection.close()
