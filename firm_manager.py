"""
helper function for retrieving a firm by ID (used in contactfunctions).
"""

import mysql.connector

def get_firm(id, connection):
    """
    returns a single row from the 'firm' table for the specified ID.
    if not found, returns None.
    """
    select_query = 'SELECT * FROM firm WHERE id=%s'
    params = (id,)

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(select_query, params)
        result = cursor.fetchone()
        cursor.close()
        return result
    except mysql.connector.Error as e:
        print(e)
        return None
