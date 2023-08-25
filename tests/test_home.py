import unittest
from io import BytesIO
from flask import Flask
from app import app

# This class contains unit tests for the home page of the application.
class TestHome(unittest.TestCase):
    # This method sets up the necessary objects for testing.
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    # This test checks if the GET request to the home page returns a 200 status code.
    def test_home_get(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    # This test checks if the POST request to the home page without a file returns a 302 status code.
    def test_home_post_no_file(self):
        result = self.app.post('/', data={})
        self.assertEqual(result.status_code, 302)

    # This test checks if the POST request to the home page with an empty filename returns a 302 status code.
    def test_home_post_empty_filename(self):
        result = self.app.post('/', data={'file': (BytesIO(b'my file contents'), '')})
        self.assertEqual(result.status_code, 302)

    # This test checks if the POST request to the home page with an unsupported file format returns an error message.
    def test_home_post_unsupported_file_format(self):
        result = self.app.post('/', data={'file': (BytesIO(b'my file contents'), 'test.pdf')})
        self.assertEqual(result.data, b'Unsupported file format. Please upload a .txt file.')

# This is the main entry point for running the tests.
if __name__ == '__main__':
    unittest.main()