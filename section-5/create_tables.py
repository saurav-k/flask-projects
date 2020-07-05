import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (" \
               "id INTEGER PRIMARY KEY," \
               "username text," \
               "password text) "

cursor.execute(create_table)
# cursor.execute("INSERT INTO users VALUES (null , 'bob', 'abcd')")
create_item_table = "CREATE TABLE IF NOT EXISTS items (" \
               "name text," \
               "price real)"
cursor.execute(create_item_table)
# cursor.execute("INSERT INTO items VALUES ('test', 10.44)")
# Cleaning table
# cleanup_query = "DELETE FROM users"
# cursor.execute(cleanup_query)
# cleanup_query = "DELETE FROM items"
# cursor.execute(cleanup_query)
connection.commit()
connection.close()
