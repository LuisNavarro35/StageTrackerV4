import config

import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

    if connection.is_connected():
        print("✅ Successfully connected to MySQL database")
        db_info = connection.server_info
        print("MySQL Server version:", db_info)

except Error as e:
    print("❌ Error while connecting to MySQL:", e)

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")
