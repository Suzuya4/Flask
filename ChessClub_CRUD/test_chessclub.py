import unittest
from flask import Flask
from flask_testing import TestCase
from chess_club import app, mysql  # Import the Flask app and MySQL instance

# Define a test class that inherits from Flask-Testing's TestCase
class TestApp(TestCase):

    # Override create_app method to configure the Flask app for testing
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['DEBUG'] = False  # Disable debug mode
        app.config['MYSQL_DB'] = 'db'  # Use a different database for testing
        return app

    # Set up method to run before each test
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

    # Optional tearDown method to run after each test
    # def tearDown(self):
    #     # Drop the test database table
    #     with app.app_context():
    #         cur = mysql.connection.cursor()
    #         cur.execute("DROP TABLE IF EXISTS chess_club")
    #         mysql.connection.commit()

    # Test the index route
    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the response status is OK (200)
        self.assertIn(b'chess_club', response.data)  # Check if 'chess_club' is present in the response data

    # Test the insert route
    def test_insert_route(self):
        response = self.client.post('/insert', data={
            'club_id': '300',
            'club_name': 'Test Club',
            'club_address': 'Test Address',
            'other_club_details': 'Test Details'
        })
        self.assertEqual(response.status_code, 302)  # Check if the response status is a redirect (302)

    # Test the update route
    def test_update_route(self):
        response = self.client.post('/update', data={
            'club_id': '300',
            'club_name': 'Updated Club',
            'club_address': 'Updated Address',
            'other_club_details': 'Updated Details'
        })
        self.assertEqual(response.status_code, 302)  # Check if the response status is a redirect (302)

    # Test the delete route
    def test_delete_route(self):
        response = self.client.get('/delete/300') 
        self.assertEqual(response.status_code, 302)  # Check if the response status is a redirect (302)

# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
