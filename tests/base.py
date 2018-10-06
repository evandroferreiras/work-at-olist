import unittest
from app import app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = False
        self.app = self.app.test_client()
