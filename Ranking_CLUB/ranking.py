from flask import Flask, render_template, request, url_for, flash,jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import json
import dicttoxml

# app = Flask(__name__)
# # # Load configuration from JSON file
# # with open('config.json') as config_file:
# #     config_data = json.load(config_file)

# app.secret_key = config_data.get('SECRET_KEY', 'many random bytes')

# app.config['MYSQL_HOST'] = config_data.get('MYSQL_HOST', 'localhost')
# app.config['MYSQL_USER'] = config_data.get('MYSQL_USER', 'root')
# app.config['MYSQL_PASSWORD'] = config_data.get('MYSQL_PASSWORD', 'root')
# app.config['MYSQL_DB'] = config_data.get('MYSQL_DB', 'db')
# mysql = MySQL(app)
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

@app.route('/')
def Index():
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

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        ranking_code = request.form['ranking_code']
        ranking_description = request.form['ranking_description']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ref_ranking_codes (ranking_code,ranking_description) VALUES (%s ,%s )", (ranking_code,ranking_description))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ref_ranking_codes WHERE ranking_code=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        _id = request.form['id']
        club_id = request.form['club_id']
        ranking_code = request.form['ranking_code']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']
        other_player_details = request.form['other_player_details']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE ref_ranking_codes SET club_id=%s,ranking_code=%s,address=%s, phone_number=%s, email_address=%s, other_player_details=%s
        WHERE  id=%s
        """, (club_id,ranking_code,address,phone_number, email_address, other_player_details, _id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)