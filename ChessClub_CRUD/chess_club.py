# Import necessary modules and libraries
from flask import Flask, render_template, request, url_for, flash, jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import json
import dicttoxml

# Create a Flask application
app = Flask(__name__)
app.secret_key = 'many random bytes'

# Configure MySQL connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'db'

# Initialize MySQL
mysql = MySQL(app)

# Helper function to get the desired output format from the query string
def get_output_format():
    return request.args.get('format', 'json').lower()

# Helper function to convert a dictionary to XML using dicttoxml library
def convert_to_xml(data):
    return dicttoxml.dicttoxml(data)

# Helper function for error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

# Define a route for the home page
@app.route('/')
def index():
    try:
        # Execute a SELECT query to fetch data from the 'chess_club' table
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM chess_club")
        data = cur.fetchall()
        cur.close()

        # Determine the desired output format (JSON, XML, HTML)
        output_format = get_output_format()

        if output_format == 'xml':
            # Convert data to XML and return the response
            xml_data = convert_to_xml({'chess_club': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            # Return data in JSON format
            return jsonify(chess_club=data)
        else:
            # Render an HTML template with the data
            return render_template('index.html', chess_club=data)

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Define a route for inserting data into the 'chess_club' table
@app.route('/insert', methods=['POST'])
def insert():
    try:
        # Check if the request method is POST
        if request.method == "POST":
            # Get form data from the request
            club_id = request.form['club_id']
            club_name = request.form['club_name']
            club_address = request.form['club_address']
            other_club_details = request.form['other_club_details']

            # Input validation
            if not club_id or not club_name:
                return error_response('Missing required fields', 400)

            # Execute an INSERT query to add data to the 'chess_club' table
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO chess_club (club_id, club_name, club_address, other_club_details) VALUES (%s, %s, %s, %s)",
                        (club_id, club_name, club_address, other_club_details))
            mysql.connection.commit()
            
            # Redirect to the home page after successful insertion
            return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Define a route for deleting a record from the 'chess_club' table
@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    try:
        # Execute a DELETE query to remove a record with the given club_id
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM chess_club WHERE club_id=%s", (id,))
        mysql.connection.commit()
        
        # Flash a success message and redirect to the home page
        flash("Record Has Been Deleted Successfully")
        return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Define a route for updating data in the 'chess_club' table
@app.route('/update', methods=['POST', 'GET'])
def update():
    try:
        # Check if the request method is POST
        if request.method == 'POST':
            # Get form data from the request
            club_id = request.form['club_id']
            club_name = request.form['club_name']
            club_address = request.form['club_address']
            other_club_details = request.form['other_club_details']

            # Input validation
            if not club_id or not club_name:
                return error_response('Missing required fields', 400)

            # Execute an UPDATE query to modify data in the 'chess_club' table
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE chess_club SET club_name=%s, club_address=%s, other_club_details=%s 
            WHERE club_id=%s
            """, (club_name, club_address, other_club_details, club_id))
            
            # Flash a success message and redirect to the home page
            flash("Data Updated Successfully")
            mysql.connection.commit()
            return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Define a route for searching data in the 'chess_club' table by club_id
@app.route('/search/<string:id>', methods=['GET'])
def search(id):
    try:
        # Execute a SELECT query to fetch data based on the given club_id
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM chess_club WHERE club_id=%s", (id,))
        data = cur.fetchall()
        cur.close()

        # Determine the desired output format (JSON, XML, HTML)
        output_format = get_output_format()

        if output_format == 'xml':
            # Convert data to XML and return the response
            xml_data = convert_to_xml({'players': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            # Return data in JSON format
            return jsonify(players=data)
        else:
            # Render an HTML template with the data
            return render_template('index.html', players=data)

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
