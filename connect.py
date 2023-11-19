import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='password',
        database='fyp'
    )
    return conn
