import unittest
import os
import werkzeug

# Monkey-patch werkzeug to add __version__ if not present.
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '3.0.0'  # Dummy version for compatibility.

from app import app

class TestAppEndpoints(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    def test_get_root(self):
        # Test GET request returns 200 and has the investment input form.
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Enter Investment Amount", response.data)

    def test_post_investment(self):
        # Test POST request with an example investment returns expected text.
        response = self.app.post("/", data=dict(investment="1000"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Individual Asset Predictions", response.data)
        self.assertIn(b"Portfolio Predicted Value", response.data)

if __name__ == '__main__':
    # These tests were generated with the help of AI to speed up development while ensuring robust endpoint testing.
    unittest.main()