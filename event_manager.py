from database_helper import get_db_connection
from flask import jsonify, request
import mysql.connector

def get_events():
    """
    retrieves all events from the 'events' table in the database.
    returns a JSON array of event objects.
    """
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    # execute the query to fetch all events
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events")
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    # return the result as a JSON response
    return jsonify(result)

def save_event(data):
    """
    inserts a new event into the 'events' table.
    returns a success message or an error if something goes wrong.
    """
    if not 'id' in data or not 'name' in data or not 'time_start' in data:
        return jsonify({'error': 'Missing required data'}), 400
    
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500

    description = data.get('description', None)
    time_end = data.get('time_end', None)
    
    try:
        id = int(data['id'])
        if id < 1:
            return jsonify({'error': 'ID must be greater than 0'}), 400

        # prepare the SQL query and parameters
        insert_query = 'INSERT INTO events(id, name, description, time_start, time_end) VALUES(%s, %s, %s, %s, %s)'
        params = (data['id'], data['name'], description, data['time_start'], time_end)

        try:
            cursor = connection.cursor()
            cursor.execute(insert_query, params)
            connection.commit()
        except mysql.connector.Error as e:
            print(e)
            return jsonify({'error': 'Failed to save the event'}), 500
        finally:
            cursor.close()
            connection.close()
        return jsonify({'message': 'Event successfully added'}), 200
    except ValueError:
        return jsonify({'error': 'ID must be an integer'}), 400

def update_event():
    """
    placeholder for updating an event.
    currently raises a NotImplementedError because the feature is not implemented.
    """
    raise NotImplementedError()

def delete_event(event_id):
    """
    deletes an event with the specified ID from the 'events' table.
    returns a success message or an error if something goes wrong.
    """
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection error'}), 500
    
    delete_query = 'DELETE FROM events WHERE id=%s'
    params = (event_id,)

    try:
        cursor = connection.cursor()
        cursor.execute(delete_query, params)
        connection.commit()
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to delete the event'}), 500
    finally:
        cursor.close()
        connection.close()
    return jsonify({'message': 'Event successfully deleted'}), 200
