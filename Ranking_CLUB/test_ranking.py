import unittest
from flask import Flask
from flask_testing import TestCase
from ranking import app  # Replace 'your_flask_app_file' with the actual filename of your Flask app
import json
import xml.etree.ElementTree as ET

# Define a test class that inherits from Flask-Testing's TestCase
class TestApp(TestCase):
    
    # Custom assertion method for JSON responses
    def assert_json(self, response):
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    # Custom assertion method for XML responses
    def assert_xml(self, response):
        data = ET.fromstring(response.data)
        self.assertIsInstance(data, ET.Element)

    # Define a method to create the Flask app for testing
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    # Test case for the default format of the index route
    def test_index_default_format(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_json(response)

    # Test case for the JSON format of the index route
    def test_index_json_format(self):
        response = self.client.get('/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assert_json(response)

    # Test case for the XML format of the index route
    def test_index_xml_format(self):
        response = self.client.get('/?format=xml')
        self.assertEqual(response.status_code, 200)
        self.assert_xml(response)

    # Test case for inserting data into the database
    def test_insert(self):
        response = self.client.post('/insert', data={
            'ranking_code': '6',
            'ranking_description':'Beginner',
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful insertion

    # Test case for updating data in the database
    def test_update(self):
        response = self.client.post('/update', data={
            'ranking_code': '6',
            'ranking_description':'Basic Beginner',
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful update

    # Test case for deleting a record from the database
    def test_delete(self):
        response = self.client.get('/delete/6')  # Replace '1' with an actual ranking_code
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful deletion

# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
