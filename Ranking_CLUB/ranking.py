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
        cur.execute("SELECT * FROM ref_ranking_codes")
        data = cur.fetchall()
        cur.close()

        output_format = get_output_format()

        if output_format == 'xml':
            xml_data = convert_to_xml({'ref_ranking_codes': data})
            return app.response_class(xml_data, content_type='application/xml')
        elif output_format == 'json':
            return jsonify(ref_ranking_codes=data)
        else:
            # Render HTML template
            return render_template('index.html', ref_ranking_codes=data)

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/insert', methods=['POST'])
def insert():
    try:
        if request.method == "POST":
            flash("Data Inserted Successfully")
            ranking_code = request.form['ranking_code']
            ranking_description = request.form['ranking_description']

            # Input validation (customize these conditions)
            if not ranking_code or not ranking_description:
                return error_response('Missing required fields', 400)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO ref_ranking_codes (ranking_code,ranking_description) VALUES (%s ,%s )", (ranking_code, ranking_description))
            mysql.connection.commit()
            return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    try:
        flash("Record Has Been Deleted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM ref_ranking_codes WHERE ranking_code=%s", (id,))
        mysql.connection.commit()
        return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)

@app.route('/update', methods=['POST', 'GET'])
def update():
    try:
        if request.method == 'POST':
            ranking_code = request.form['ranking_code']
            ranking_description = request.form['ranking_description']

            # Input validation (customize these conditions)
            if not ranking_code or not ranking_description:
                return error_response('Missing required fields', 400)

            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE ref_ranking_codes SET ranking_description=%s
            WHERE ranking_code=%s
            """, (ranking_description, ranking_code))
            flash("Data Updated Successfully")
            mysql.connection.commit()
            return redirect(url_for('index'))

    except Exception as e:
        return error_response(str(e), 500)

if __name__ == "__main__":
    app.run(debug=True)
