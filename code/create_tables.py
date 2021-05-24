import mysql.connector

connection = mysql.connector.connect(
    user = "marko",
    password ="marko123!!",
    host ="localhost",
    database = "api"
)

cursor = connection.cursor()

create_table = "CREATE TABLE users (id integer primary KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

connection.commit()
connection.close()

