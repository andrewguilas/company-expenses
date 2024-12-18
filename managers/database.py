from datetime import datetime
from enum import Enum
import json
import sqlite3
from managers.entry import Entry

class DuplicateEntryError(Exception):
    def __init__(self, message="Duplicate entry found."):
        self.message = message
        super().__init__(self.message)

class Database:
    def __init__(self):
        self.db_filename = self.load_config()\

        try:
            self.connection = sqlite3.connect(self.db_filename)
        except sqlite3.Error as error_message:
            print(f"Database connection error: {error_message}")
            raise

        self.cursor = self.connection.cursor()
        self.create_tables()

    def load_config(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
                return config.get("db_filename", "database.db")
        except FileNotFoundError:
            print("Config file not found, using default settings.")
            return "database.db"

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('EXPENSE', 'REVENUE')),
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                location TEXT NOT NULL
            )
        """)
        self.connection.commit()

# database.py

    def add_entry(self, entry):
        # Check for duplicate
        self.cursor.execute("""
            SELECT 1 FROM entries WHERE date=? AND type=? AND category=? AND description=? AND amount=? AND location=?
        """, (entry.date, entry.type.value, entry.category, entry.description, entry.amount, entry.location))
        
        if self.cursor.fetchone():  # Duplicate found
            raise DuplicateEntryError(f"Duplicate entry: {entry}")
        
        self.cursor.execute("""
            INSERT INTO entries (date, type, category, description, amount, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (entry.date, entry.type.value, entry.category, entry.description, entry.amount, entry.location))
        self.connection.commit()
        entry.id = self.cursor.lastrowid

    def get_entries(self, entry_type):
        with self.connection:
            self.cursor.execute("SELECT * FROM entries WHERE type=?", (entry_type,))
            rows = self.cursor.fetchall()
        return [Entry(datetime.strptime(row[1], "%Y-%m-%d").date(), row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def get_expenses(self):
        return self.get_entries('EXPENSE')

    def get_revenues(self):
        return self.get_entries('REVENUE')

    def update_entry(self, entry):
        self.cursor.execute("""
            UPDATE entries
            SET date=?, type=?, category=?, description=?, amount=?, location=?
            WHERE id=?
        """, (entry.date, entry.type.value, entry.category, entry.description, entry.amount, entry.location, entry.id))
        self.connection.commit()

    def delete_entry(self, entry):
        self.cursor.execute("""
            DELETE FROM entries WHERE id=?
        """, (entry.id,))
        self.connection.commit()

    def get_locations(self):
        with self.connection:
            self.cursor.execute("SELECT DISTINCT location FROM entries")
            rows = self.cursor.fetchall()

        return [row[0] for row in rows]

    def get_categories(self):
        with self.connection:
            self.cursor.execute("SELECT DISTINCT category FROM entries")
            rows = self.cursor.fetchall()

        return [row[0] for row in rows]

    def close(self):
        self.cursor.close()
        self.connection.close()
