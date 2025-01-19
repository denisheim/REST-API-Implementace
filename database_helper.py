"""
holds the database configuration.
"""

import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rest_api'
}

def get_db_connection():
    """
    Creates a connection to the MySQL database using db_config.
    Returns the connection object, or None if it fails.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        print("Database connection error:", e)
        return None
