from datetime import datetime
import unittest

from managers.database import Database, DuplicateEntryError
from managers.entry import Entry, EntryType

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database(db_filename=":memory:")

    def tearDown(self):
        self.database.close()

    def test_add_entry(self):
        entry = Entry(
            date=datetime(2023, 12, 18).date(),
            type=EntryType.EXPENSE,
            category="food",
            description="strawberry cheesecake",
            amount=15.75,
            location="new york"
        )
        self.database.add_entry(entry)
        entries = self.database.get_entries()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].description, "strawberry cheesecake")

    def test_duplicate_entry(self):
        entry = Entry(
            date=datetime(2023, 12, 18).date(),
            type=EntryType.EXPENSE,
            category="food",
            description="strawberry cheesecake",
            amount=15.75,
            location="new york"
        )
        self.database.add_entry(entry)
        with self.assertRaises(DuplicateEntryError):
            self.database.add_entry(entry)

    def test_get_entries(self):
        entry1 = Entry(
            date=datetime(2023, 12, 18).date(),
            type=EntryType.EXPENSE,
            category="food",
            description="strawberry cheesecake",
            amount=15.75,
            location="new york"
        )
        entry2 = Entry(
            date=datetime(2023, 12, 19).date(),
            type=EntryType.EXPENSE,
            category="food",
            description="chocolate strawberry cheesecake",
            amount=16.75,
            location="new york"
        )
        self.database.add_entry(entry1)
        self.database.add_entry(entry2)
        entries = self.database.get_entries()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[1].type, EntryType.REVENUE)
