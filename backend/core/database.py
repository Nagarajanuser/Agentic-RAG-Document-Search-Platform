import mysql.connector
from .config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

db_config = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
}


def get_db_cursor():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    return conn, cursor
