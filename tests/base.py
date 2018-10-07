import unittest
from app import app
from app.core.db import init_db


class BaseTestCase(unittest.TestCase):
    def setUp(self, db_connection=None):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = False
        if db_connection:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
            init_db(self.app)
        self.app = self.app.test_client()
