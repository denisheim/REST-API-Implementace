"""
helper functions for managing contact info in the 'firm' table.
"""

from database_helper import get_db_connection
from flask import jsonify
import mysql.connector
from firm_manager import get_firm

def get_contacts(firm_id):
    """
    returns contact information (email, phone, name, surname)
    for a specific firm.
    """
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500

    select_query = 'SELECT email, phone, name, surname FROM firm WHERE firm.id=%s'
    params = (firm_id,)

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(select_query, params)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return jsonify(result), 200
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Could not retrieve contacts'}), 500

def save_contacts(firm_id, data):
    """
    overwrites the contact data (email, phone, name, surname) for a given firm.
    requires all keys to be present in the JSON (email, phone, name, surname).
    """
    required_keys = ('email', 'phone', 'name', 'surname')
    if not all(k in data for k in required_keys):
        return jsonify({'error': 'Missing data'}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500

    update_query = 'UPDATE firm SET email=%s, phone=%s, name=%s, surname=%s WHERE id=%s'
    params = (data['email'], data['phone'], data['name'], data['surname'], firm_id)

    try:
        cursor = connection.cursor()
        cursor.execute(update_query, params)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Contacts saved successfully'}), 200
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to save contacts'}), 500

def update_contacts(firm_id, data):
    """
    updates whichever of the four fields are provided in 'data'
    (email, phone, name, surname).
    if none are provided, returns a 400 error.
    """
    if not any(k in data for k in ('email', 'phone', 'name', 'surname')):
        return jsonify({'error': 'No fields to update'}), 400

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500

    try:
        cursor = connection.cursor()
        if 'email' in data:
            cursor.execute('UPDATE firm SET email=%s WHERE id=%s', (data['email'], firm_id))
        if 'phone' in data:
            cursor.execute('UPDATE firm SET phone=%s WHERE id=%s', (data['phone'], firm_id))
        if 'name' in data:
            cursor.execute('UPDATE firm SET name=%s WHERE id=%s', (data['name'], firm_id))
        if 'surname' in data:
            cursor.execute('UPDATE firm SET surname=%s WHERE id=%s', (data['surname'], firm_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Contacts updated successfully'}), 200
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to update contacts'}), 500

def delete_contacts(firm_id):
    """
    sets email, phone, name, and surname to NULL for the specified firm.
    """
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500

    # Check if firm exists first
    if get_firm(firm_id, connection) is None:
        return jsonify({'error': 'Firm not found'}), 404

    update_query = 'UPDATE firm SET email=NULL, phone=NULL, name=NULL, surname=NULL WHERE id=%s'
    params = (firm_id,)

    try:
        cursor = connection.cursor()
        cursor.execute(update_query, params)
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Contacts deleted successfully'}), 200
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to delete contacts'}), 500
