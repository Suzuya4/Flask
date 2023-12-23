
# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, request, url_for, flash, jsonify, make_response
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import json
import dicttoxml

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'many random bytes'  # Secret key for session management

# Configure MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'db'

# Initialize MySQL
mysql = MySQL(app)

# Function to get the desired output format (JSON, XML, or HTML)
def get_output_format():
    return request.args.get('format', 'json').lower()

# Function to convert dictionary to XML using dicttoxml library
def convert_to_xml(data):
    return dicttoxml.dicttoxml(data)

# Helper function for error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

# Route to display the list of players
@app.route('/')
def index():
    try:
        # Fetch data from MySQL database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM players")
        data = cur.fetchall()
        cur.close()

        # Determine the desired output format (JSON, XML, or HTML)
        output_format = get_output_format()

        if output_format == 'xml':
            # Convert data to XML and return the response
            xml_data = convert_to_xml({'players': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            # Return JSON response
            return jsonify(players=data)
        else:
            # Render HTML template with player data
            return render_template('index.html', players=data)

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Route to insert new player data
@app.route('/insert', methods=['POST'])
def insert():
    try:
        if request.method == "POST":
            # Get data from the form submission
            _id = request.form['id']
            club_id = request.form['club_id']
            ranking_code = request.form['ranking_code']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email_address = request.form['email_address']
            other_player_details = request.form['other_player_details']

            # Input validation (customize these conditions as needed)
            if not _id or not club_id or not ranking_code:
                return error_response('Missing required fields', 400)

            # Insert data into the players table
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO players (id,club_id,ranking_code,address, phone_number, email_address, other_player_details) VALUES (%s ,%s , %s , %s , %s, %s, %s)", (_id, club_id, ranking_code, address, phone_number, email_address, other_player_details))
            mysql.connection.commit()
            flash("Data Inserted Successfully")
            return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Route to delete a player record
@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    try:
        # Delete player record with the specified ID
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM players WHERE id=%s", (id,))
        mysql.connection.commit()
        flash("Record Has Been Deleted Successfully")
        return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Route to update player data
@app.route('/update', methods=['POST', 'GET'])
def update():
    try:
        if request.method == 'POST':
            # Get data from the form submission
            _id = request.form['id']
            club_id = request.form['club_id']
            ranking_code = request.form['ranking_code']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email_address = request.form['email_address']
            other_player_details = request.form['other_player_details']

            # Input validation (customize these conditions as needed)
            if not _id or not club_id or not ranking_code:
                return error_response('Missing required fields', 400)

            # Update player data in the players table
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE players SET club_id=%s,ranking_code=%s,address=%s, phone_number=%s, email_address=%s, other_player_details=%s
            WHERE  id=%s
            """, (club_id, ranking_code, address, phone_number, email_address, other_player_details, _id))
            flash("Data Updated Successfully")
            mysql.connection.commit()
            return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Route to search for a player by ID
@app.route('/search/<string:id>', methods=['GET'])
def search(id):
    try:
        # Fetch player data with the specified ID
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM players WHERE id=%s",(id))
        data = cur.fetchall()
        cur.close()

        # Determine the desired output format (JSON, XML, or HTML)
        output_format = get_output_format()

        if output_format == 'xml':
            # Convert data to XML and return the response
            xml_data = convert_to_xml({'players': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            # Return JSON response
            return jsonify(players=data)
        else:
            # Render HTML template with player data
            return render_template('index.html', players=data)

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
