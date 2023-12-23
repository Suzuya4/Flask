import unittest
from flask import Flask
from flask_testing import TestCase
from chess_club import app, mysql  # Replace 'your_flask_app' with the actual name of your Flask app file

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['DEBUG'] = False  # Disable debug mode
        app.config['MYSQL_DB'] = 'db'  # Use a different database for testing
        return app

    def setUp(self):
        # Create a test client
        self.client = self.app.test_client()
        # Create a test database table
        with app.app_context():
            cur = mysql.connection.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chess_club (
                    club_id INT PRIMARY KEY,
                    club_name VARCHAR(255) NOT NULL,
                    club_address VARCHAR(255) NOT NULL,
                    other_club_details VARCHAR(255)
                )
            """)
            mysql.connection.commit()

    # def tearDown(self):
    #     # Drop the test database table
    #     with app.app_context():
    #         cur = mysql.connection.cursor()
    #         cur.execute("DROP TABLE IF EXISTS chess_club")
    #         mysql.connection.commit()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'chess_club', response.data)

    def test_insert_route(self):
        response = self.client.post('/insert', data={
            'club_id': '300',
            'club_name': 'Test Club',
            'club_address': 'Test Address',
            'other_club_details': 'Test Details'
        })
        self.assertEqual(response.status_code, 302) 

    def test_update_route(self):
        response = self.client.post('/update', data={
            'club_id': '300',
            'club_name': 'Updated Club',
            'club_address': 'Updated Address',
            'other_club_details': 'Updated Details'
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_route(self):
        response = self.client.get('/delete/300') 
        self.assertEqual(response.status_code, 302)



if __name__ == '__main__':
    unittest.main()
