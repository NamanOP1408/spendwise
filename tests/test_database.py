"""Small automated tests for core storage behavior."""

import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_path = database.DB_PATH
        database.DB_PATH = Path(self.temp_dir.name) / "test.db"
        database.initialize_database()

    def tearDown(self):
        database.DB_PATH = self.original_path
        self.temp_dir.cleanup()

    def test_add_and_fetch_expense(self):
        expense_id = database.add_expense(Decimal("12.50"), "food", "Tea", "2026-10-20")
        items = database.fetch_expenses()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], expense_id)
        self.assertEqual(items[0]["amount_cents"], 1250)
        self.assertEqual(items[0]["category"], "Food")

    def test_delete_expense(self):
        expense_id = database.add_expense(Decimal("99"), "Travel", "Metro", "2026-10-20")
        self.assertTrue(database.delete_expense(expense_id))
        self.assertFalse(database.delete_expense(expense_id))
        self.assertEqual(database.fetch_expenses(), [])


if __name__ == "__main__":
    unittest.main()
