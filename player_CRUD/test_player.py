import unittest
from flask import Flask
from flask_testing import TestCase
from player import app  # Import the Flask app to be tested
import json
import xml.etree.ElementTree as ET 

# Define a test class that inherits from Flask-Testing's TestCase
class TestApp(TestCase):
    
    # Custom assertion to check if the response contains JSON data
    def assert_json(self, response):
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    # Custom assertion to check if the response contains XML data
    def assert_xml(self, response):
        data = ET.fromstring(response.data)
        self.assertIsInstance(data, ET.Element)

    # Method to create the Flask app for testing
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    # Test case to check the default format of the index route
    def test_index_default_format(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  # Expecting a successful response
        self.assert_json(response)  # Check if the response contains JSON data

    # Test case to check the JSON format of the index route
    def test_index_json_format(self):
        response = self.client.get('/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assert_json(response)

    # Test case to check the XML format of the index route
    def test_index_xml_format(self):
        response = self.client.get('/?format=xml')
        self.assertEqual(response.status_code, 200)
        self.assert_xml(response)

    # Test case to check the insertion of new player data
    def test_insert(self):
        response = self.client.post('/insert', data={
            'id': '444',
            'club_id': '4',
            'ranking_code': '3',
            'address':'PPC',
            'phone_number': '0999999999',
            'email_address': 'Example@gmial.com',
            'other_player_details': 'Last Year Champion'
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful insertion

    # Test case to check the updating of player data
    def test_update(self):
        response = self.client.post('/update', data={
            'id': '444',  # Replace '1' with an actual player_id
            'club_id': '6',
            'ranking_code': '2',
            'address': 'ICT',
            'phone_number': '0888888888',
            'email_address': 'Admin@gmail.com',
            'other_player_details': 'Defending Champion 2020'
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful update

    # Test case to check the deletion of player data
    def test_delete(self):
        response = self.client.get('/delete/444')  # Replace '1' with an actual player_id
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful deletion

# Run the tests if this script is the main entry point
if __name__ == '__main__':
    unittest.main()
