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
        self.assertEqual(entries[1].type, "EXPENSE")

    def test_get_expenses_and_revenues(self):
        expense = Entry(
            date=datetime(2023, 12, 18).date(),
            type=EntryType.EXPENSE,
            category="Food",
            description="Lunch at cafe",
            amount=15.75,
            location="City Center"
        )
        revenue = Entry(
            date=datetime(2023, 12, 19).date(),
            type=EntryType.REVENUE,
            category="Salary",
            description="Monthly salary",
            amount=2500,
            location="Workplace"
        )
        self.database.add_entry(expense)
        self.database.add_entry(revenue)

        expenses = self.database.get_expenses()
        revenues = self.database.get_revenues()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].category, "Food")
        self.assertEqual(len(revenues), 1)
        self.assertEqual(revenues[0].category, "Salary")

    def test_update_entry(self):
        entry = Entry(
            date=datetime(2023, 12, 18).date(),
            type=EntryType.EXPENSE,
            category="Food",
            description="Lunch at cafe",
            amount=15.75,
            location="City Center"
        )
        self.database.add_entry(entry)
        entry_id = entry.id

        entry.description = "Dinner at cafe"
        entry.amount = 25.50
        self.database.update_entry(entry)

        updated_entry = self.database.get_entries()[0]
        self.assertEqual(updated_entry.id, entry_id)
        self.assertEqual(updated_entry.description, "Dinner at cafe")
        self.assertEqual(updated_entry.amount, 25.50)

    def test_delete_entry(self):
        entry = Entry(
            date=datetime(2023, 12, 18).date(),
            type=EntryType.EXPENSE,
            category="Food",
            description="Lunch at cafe",
            amount=15.75,
            location="City Center"
        )
        self.database.add_entry(entry)
        self.database.delete_entry(entry)
        entries = self.database.get_entries()
        self.assertEqual(len(entries), 0)

    def test_get_locations(self):
        entry1 = Entry(
            date=datetime(2023, 12, 18).date(),
            type=EntryType.EXPENSE,
            category="Food",
            description="Lunch at cafe",
            amount=15.75,
            location="City Center"
        )
        entry2 = Entry(
            date=datetime(2023, 12, 19).date(),
            type=EntryType.REVENUE,
            category="Salary",
            description="Monthly salary",
            amount=2500,
            location="Workplace"
        )
        self.database.add_entry(entry1)
        self.database.add_entry(entry2)

        locations = self.database.get_locations()
        self.assertIn("City Center", locations)
        self.assertIn("Workplace", locations)
