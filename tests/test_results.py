import unittest
from app import app

class TestResults(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def test_results_get_status_code(self):
        result = self.app.get('/results')
        self.assertEqual(result.status_code, 200)

    def test_results_get_content_type(self):
        result = self.app.get('/results')
        self.assertEqual(result.content_type, 'text/html; charset=utf-8')

    def test_results_get_data(self):
        result = self.app.get('/results')
        self.assertIn(b'Results', result.data)

if __name__ == '__main__':
    unittest.main()