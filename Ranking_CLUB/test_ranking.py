import unittest
from flask import Flask
from flask_testing import TestCase
from ranking import app  # Replace 'your_flask_app_file' with the actual filename of your Flask app
import json
import xml.etree.ElementTree as ET 
class TestApp(TestCase):
    
    def assert_json(self, response):
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)

    def assert_xml(self, response):
        data = ET.fromstring(response.data)
        self.assertIsInstance(data, ET.Element)
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def test_index_default_format(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_json(response)

    def test_index_json_format(self):
        response = self.client.get('/?format=json')
        self.assertEqual(response.status_code, 200)
        self.assert_json(response)

    def test_index_xml_format(self):
        response = self.client.get('/?format=xml')
        self.assertEqual(response.status_code, 200)
        self.assert_xml(response)

    def test_insert(self):
        response = self.client.post('/insert', data={
            'ranking_code': '6',
            'ranking_description':'Beginner',
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful insertion

    def test_update(self):
        response = self.client.post('/update', data={
            'ranking_code': '6',
            'ranking_description':'Basic Beginner',
        })
        self.assertEqual(response.status_code, 302) 

    def test_delete(self):
        response = self.client.get('/delete/6')  # Replace '1' with an actual customer_id
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful deletion

 # Expecting a redirect after successful update>

if __name__ == '__main__':
    unittest.main()