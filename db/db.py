import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_NAME, DB_PASS, DB_USER

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_read_query(query):
    connection = create_connection(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_query(query):
    connection = create_connection(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")