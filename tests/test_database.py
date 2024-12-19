import os
import unittest

from managers.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database(db_filename=":memory:")

    def tearDown(self):
        self.database.close()

    def test_add_entry(self):
        pass
