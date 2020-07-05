import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (" \
               "id int," \
               "username text," \
               "password text) "

cursor.execute(create_table)
# Insert one element
user = (1, "jose", "abcd")
insert_query = "INSERT INTO users  VALUES  (?, ?, ?)"
cursor.execute(insert_query, user)

# Insert a list
users = [
        (2, "jose", "abcd"),
        (3, "jose", "abcd")
]
cursor.executemany(insert_query, users)

# Selecting data from table
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# Cleaning table
# cleanup_query = "DELETE FROM users"
# cursor.execute(cleanup_query)
connection.commit()
connection.close()