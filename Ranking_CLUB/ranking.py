# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, request, url_for, flash, jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import json
import dicttoxml

# Create a Flask application
app = Flask(__name__)

# Set a secret key for the app
app.secret_key = 'many random bytes'

# Configure MySQL database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'db'

# Initialize MySQL
mysql = MySQL(app)

# Define a function to get the output format (JSON or XML) from the query string
def get_output_format():
    return request.args.get('format', 'json').lower()

# Define a function to convert a dictionary to XML using the dicttoxml library
def convert_to_xml(data):
    return dicttoxml.dicttoxml(data)

# Define a helper function for error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

# Define the route for the home page
@app.route('/')
def index():
    try:
        # Connect to the database and fetch all records from the 'ref_ranking_codes' table
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM ref_ranking_codes")
        data = cur.fetchall()
        cur.close()

        # Determine the desired output format (JSON, XML, or HTML)
        output_format = get_output_format()

        # Handle different output formats
        if output_format == 'xml':
            xml_data = convert_to_xml({'ref_ranking_codes': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            return jsonify(ref_ranking_codes=data)
        else:
            # Render HTML template
            return render_template('index.html', ref_ranking_codes=data)

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Define the route for inserting data into the database
@app.route('/insert', methods=['POST'])
def insert():
    try:
        # Check if the request method is POST
        if request.method == "POST":
            flash("Data Inserted Successfully")
            ranking_code = request.form['ranking_code']
            ranking_description = request.form['ranking_description']

            # Input validation
            if not ranking_code or not ranking_description:
                return error_response('Missing required fields', 400)

            # Connect to the database, insert data, and commit the changes
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO ref_ranking_codes (ranking_code,ranking_description) VALUES (%s ,%s )", (ranking_code, ranking_description))
            mysql.connection.commit()
            
            # Redirect to the home page
            return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Define the route for deleting a record from the database
@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    try:
        flash("Record Has Been Deleted Successfully")
        
        # Connect to the database, delete the record, and commit the changes
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM ref_ranking_codes WHERE ranking_code=%s", (id,))
        mysql.connection.commit()
        
        # Redirect to the home page
        return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Define the route for updating data in the database
@app.route('/update', methods=['POST', 'GET'])
def update():
    try:
        # Check if the request method is POST
        if request.method == 'POST':
            ranking_code = request.form['ranking_code']
            ranking_description = request.form['ranking_description']

            # Input validation
            if not ranking_code or not ranking_description:
                return error_response('Missing required fields', 400)

            # Connect to the database, update data, and commit the changes
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE ref_ranking_codes SET ranking_description=%s
            WHERE ranking_code=%s
            """, (ranking_description, ranking_code))
            
            flash("Data Updated Successfully")
            mysql.connection.commit()
            
            # Redirect to the home page
            return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Define the route for searching a record in the database
@app.route('/search/<string:id>', methods=['GET'])
def search(id):
    try:
        # Connect to the database and fetch records matching the given ID
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM ref_ranking_codes WHERE ranking_code=%s", (id,))
        data = cur.fetchall()
        cur.close()

        # Determine the desired output format (JSON, XML, or HTML)
        output_format = get_output_format()

        # Handle different output formats
        if output_format == 'xml':
            xml_data = convert_to_xml({'players': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            return jsonify(players=data)
        else:
            # Render HTML template
            return render_template('index.html', players=data)

    except Exception as e:
        # Handle exceptions and return an error response
        return error_response(str(e), 500)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
