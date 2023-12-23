from flask import Flask, render_template, request, url_for, flash, jsonify, make_response
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
        cur.execute("SELECT * FROM players")
        data = cur.fetchall()
        cur.close()

        output_format = get_output_format()

        if output_format == 'xml':
            xml_data = convert_to_xml({'players': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            return jsonify(players=data)
        else:
            # Render HTML template
            return render_template('index.html', players=data)

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/insert', methods=['POST'])
def insert():
    try:
        if request.method == "POST":
            _id = request.form['id']
            club_id = request.form['club_id']
            ranking_code = request.form['ranking_code']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email_address = request.form['email_address']
            other_player_details = request.form['other_player_details']

            # Input validation (you can customize these conditions)
            if not _id or not club_id or not ranking_code:
                return error_response('Missing required fields', 400)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO players (id,club_id,ranking_code,address, phone_number, email_address, other_player_details) VALUES (%s ,%s , %s , %s , %s, %s, %s)", (_id, club_id, ranking_code, address, phone_number, email_address, other_player_details))
            mysql.connection.commit()
            flash("Data Inserted Successfully")
            return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM players WHERE id=%s", (id,))
        mysql.connection.commit()
        flash("Record Has Been Deleted Successfully")
        return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/update', methods=['POST', 'GET'])
def update():
    try:
        if request.method == 'POST':
            _id = request.form['id']
            club_id = request.form['club_id']
            ranking_code = request.form['ranking_code']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email_address = request.form['email_address']
            other_player_details = request.form['other_player_details']

            # Input validation (you can customize these conditions)
            if not _id or not club_id or not ranking_code:
                return error_response('Missing required fields', 400)

            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE players SET club_id=%s,ranking_code=%s,address=%s, phone_number=%s, email_address=%s, other_player_details=%s
            WHERE  id=%s
            """, (club_id, ranking_code, address, phone_number, email_address, other_player_details, _id))
            flash("Data Updated Successfully")
            mysql.connection.commit()
            return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)



@app.route('/search/<string:id>', methods=['GET'])
def search(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM players WHERE id=%s",(id))
        data = cur.fetchall()
        cur.close()

        output_format = get_output_format()

        if output_format == 'xml':
            xml_data = convert_to_xml({'players': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            return jsonify(players=data)
        else:
            # Render HTML template
            return render_template('index.html', players=data)

    except Exception as e:
        return error_response(str(e), 500)



if __name__ == "__main__":
    app.run(debug=True)
