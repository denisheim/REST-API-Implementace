"""
application handles:
 - Firms: listing, saving, importing/exporting
 - Contacts (for a specific firm)
 - Upload of business cards
 - Columns show/hide
"""

from flask import Flask, request, jsonify
import mysql.connector
import os

from contact_manager import *
from firm_manager import get_firm
from database_helper import get_db_connection

app = Flask(__name__)

# FIRMS: listing, saving, export/import

@app.route('/firms/list', methods=['GET'])
def list_firms():
    """
    returns a list of all firms from the 'firm' table.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM firm")
        firms = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(firms), 200
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to retrieve firms'}), 500

@app.route('/firms/save', methods=['POST'])
def save_firm():
    """
    inserts a new firm into the 'firm' table.
    expects JSON in the request body with various fields.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = """
            INSERT INTO firm (
                active, name, surname, email, phone, subject_id, source,
                date_of_contact, date_of_2_contact, date_of_meeting, result,
                workshop, brigade, practice, cv, note, c12, c13, c14, c15
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            data.get('active', 1),
            data.get('name'),
            data.get('surname'),
            data.get('email'),
            data.get('phone'),
            data.get('subject_id'),
            data.get('source'),
            data.get('date_of_contact'),
            data.get('date_of_2_contact'),
            data.get('date_of_meeting'),
            data.get('result'),
            data.get('workshop'),
            data.get('brigade'),
            data.get('practice'),
            data.get('cv'),
            data.get('note'),
            data.get('c12'),
            data.get('c13'),
            data.get('c14'),
            data.get('c15')
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Firm saved successfully'}), 201
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to save firm'}), 500

@app.route('/data/import', methods=['POST'])
def import_data():
    """
    example endpoint for importing data.
    currently just returns a success message.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        return jsonify({'message': 'Data imported successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to import data'}), 500

@app.route('/data/export', methods=['GET'])
def export_data():
    """
    example endpoint for exporting data from the 'firm' table.
    returns all rows in JSON format.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM firm")
        firms = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(firms), 200
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to export data'}), 500

# BUSINESS CARD upload

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/business_cards/upload', methods=['POST'])
def upload_business_card():
    """
    upload a file (business card image) to the server.
    returns a URL path to the uploaded file.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({
            'message': 'File uploaded successfully',
            'url': f'/uploads/{filename}'
        }), 201

# COLUMNS show/hide

@app.route('/columns/hide', methods=['POST'])
def hide_column():
    """
    sets the 'hidden' field to 1 for a specified column ID.
    expects JSON with {'column_id': someInt}.
    """
    data = request.get_json()
    if not data or 'column_id' not in data:
        return jsonify({'error': 'Column ID is required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE columns SET hidden = 1 WHERE id = %s"
        cursor.execute(sql, (data['column_id'],))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Column hidden successfully'}), 200
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to hide column'}), 500

@app.route('/columns/show', methods=['POST'])
def show_column():
    """
    sets the 'hidden' field to 0 for a specified column ID.
    expects JSON with {'column_id': someInt}.
    """
    data = request.get_json()
    if not data or 'column_id' not in data:
        return jsonify({'error': 'Column ID is required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE columns SET hidden = 0 WHERE id = %s"
        cursor.execute(sql, (data['column_id'],))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Column shown successfully'}), 200
    except mysql.connector.Error as e:
        print(e)
        return jsonify({'error': 'Failed to show column'}), 500

# CONTACTS endpoints

@app.route('/firms/<int:firm_id>/contacts/list', methods=['GET'])
def get_contacts_route(firm_id):
    """
    returns the contact information (email, phone, name, surname)
    for a specific firm (identified by firm_id).
    """
    return get_contacts(firm_id)

@app.route('/firms/<int:firm_id>/contacts/save', methods=['POST'])
def save_contacts_route(firm_id):
    """
    overwrites contact data for the specified firm.
    expects JSON with keys: email, phone, name, surname.
    """
    data = request.get_json()
    return save_contacts(firm_id, data)

@app.route('/firms/<int:firm_id>/contacts/update', methods=['PUT'])
def update_contacts_route(firm_id):
    """
    partially updates contact data (email, phone, name, surname)
    for the specified firm (if provided in the request JSON).
    """
    data = request.get_json()
    return update_contacts(firm_id, data)

@app.route('/firms/<int:firm_id>/contacts/delete', methods=['DELETE'])
def delete_contacts_route(firm_id):
    """
    sets email, phone, name, surname to NULL for the specified firm.
    """
    return delete_contacts(firm_id)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8081)
