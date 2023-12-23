from flask import Flask, render_template, request, url_for, flash, jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import json
import dicttoxml

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'db'

mysql = MySQL(app)

def get_output_format():
    # Get the format parameter from the query string, default to JSON
    return request.args.get('format', 'json').lower()

def convert_to_xml(data):
    # Convert dictionary to XML using dicttoxml library
    return dicttoxml.dicttoxml(data)

# Helper function for error responses
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM chess_club")
        data = cur.fetchall()
        cur.close()

        output_format = get_output_format()

        if output_format == 'xml':
            xml_data = convert_to_xml({'chess_club': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            return jsonify(chess_club=data)
        else:
            # Render HTML template
            return render_template('index.html', chess_club=data)

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/insert', methods=['POST'])
def insert():
    try:
        if request.method == "POST":
            flash("Data Inserted Successfully")
            club_id = request.form['club_id']
            club_name = request.form['club_name']
            club_address = request.form['club_address']
            other_club_details = request.form['other_club_details']

            # Input validation (customize these conditions)
            if not club_id or not club_name:
                return error_response('Missing required fields', 400)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO chess_club (club_id,club_name,club_address,other_club_details) VALUES (%s ,%s , %s , %s)",
                        (club_id, club_name, club_address, other_club_details))
            mysql.connection.commit()
            return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM chess_club WHERE club_id=%s", (id,))
        mysql.connection.commit()
        flash("Record Has Been Deleted Successfully")
        return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/update', methods=['POST', 'GET'])
def update():
    try:
        if request.method == 'POST':
            club_id = request.form['club_id']
            club_name = request.form['club_name']
            club_address = request.form['club_address']
            other_club_details = request.form['other_club_details']

            # Input validation (customize these conditions)
            if not club_id or not club_name:
                return error_response('Missing required fields', 400)

            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE chess_club SET club_name=%s,club_address=%s, other_club_details=%s 
            WHERE  club_id=%s
            """, (club_name, club_address, other_club_details, club_id))
            flash("Data Updated Successfully")
            mysql.connection.commit()
            return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)

if __name__ == "__main__":
    app.run(debug=True)
