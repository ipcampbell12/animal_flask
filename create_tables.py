
import sqlite3

connection = sqlite3.connect('zoo.db')
cursor = connection.cursor()

create_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT, 
        password TEXT
    )
'''
cursor.execute(create_query)

create_query = '''
    CREATE TABLE IF NOT EXISTS animals (
        type TEXT, 
        quantity INT
    )
'''
cursor.execute(create_query)

connection.commit()
connection.close()