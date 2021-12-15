import sqlite3

# create a connection object that represents our database
# the first argument can be the file where we want to store our data
# if the file exists, it just connects. if not, it craetes it and then connects
conn = sqlite3.connect('db.sqlite3')
# employee.db is not something I will understand, ut is gibberish

# Next we craeate a cursor (to be able to run sql commands, using execute method)
c = conn.cursor()

c.execute("SELECT * FROM references")
print(c.fetchall())

conn.commit()
conn.close()
