import mysql.connector
from config import Config

def get_connection():
    print("HOST:", Config.MYSQL_HOST)
    print("PORT:", Config.MYSQL_PORT)
    print("DB:", Config.MYSQL_DATABASE)

    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")
    print("Connected to:", cursor.fetchone())
    cursor.close()

    return connection