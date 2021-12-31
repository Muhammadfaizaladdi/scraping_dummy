import mysql.connector 
from mysql.connector import Error
import pandas as pd

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name)
        print("MySQL database connection successfull")
    except Error as err:
        print(f"Error: {err}")
    return connection


# Fungsi Eksekusi
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query berhasil dieksekusi")
    except Error as err:
        print(f"Error: {err}")


# Fungsi Read Query
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return pd.DataFrame(result)
    except Error as err:
        print(f"Error: {err}")