import unittest
from io import BytesIO
from flask import Flask
from app import app

class TestHome(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def test_home_get(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_home_post_no_file(self):
        result = self.app.post('/', data={})
        self.assertEqual(result.status_code, 302)

    def test_home_post_empty_filename(self):
        result = self.app.post('/', data={'file': (BytesIO(b'my file contents'), '')})
        self.assertEqual(result.status_code, 302)

    def test_home_post_unsupported_file_format(self):
        result = self.app.post('/', data={'file': (BytesIO(b'my file contents'), 'test.pdf')})
        self.assertEqual(result.data, b'Unsupported file format. Please upload a .txt file.')

    # Add more tests as needed...

if __name__ == '__main__':
    unittest.main()