import unittest
import pandas as pd
import benford

class TestBenford(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'numbers': [123, 456, 789, 101, 202, 303, 404, 505, 606, 707, 808, 909]})
        self.results = benford.benford_law(self.df)

    def test_benford_law(self):
        # Test if the function returns a list
        self.assertIsInstance(self.results, list)

        # Test if the function returns the correct number of digits
        self.assertEqual(len(self.results), 9)

        # Test if the function returns the correct digits
        self.assertEqual([result['digit'] for result in self.results], ['1', '2', '3', '4', '5', '6', '7', '8', '9'])

    def test_follows_benford_law(self):
        # Test if the function returns a boolean
        self.assertIsInstance(benford.follows_benford_law(self.results), bool)

if __name__ == '__main__':
    unittest.main()