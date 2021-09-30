import sqlite3

connection = sqlite3.connect('data.db')

#cursor - responsible for executing queries & store results
cursor = connection.cursor() 

#create table 
#schema-> table
create_table = "CREATE TABLE users (id int, username text, password text)"

#execute query
cursor.execute(create_table)

user = (1, 'Sukanya', 'asdb')


#insert data
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)

users = [
    (2, 'rohan', 'rohan345'),
    (3, 'joe', 'joe456')
]

cursor.executemany(insert_query, users)

#retrieve data
select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

#save changes to database
connection.commit()

#close connection
connection.close()