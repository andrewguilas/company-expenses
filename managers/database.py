from datetime import datetime
import json
import sqlite3
from managers.entry import Entry

class Database:
    def __init__(self):
        self.db_filename = self.load_config()
        self.connection = sqlite3.connect(self.db_filename)
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

    def add_entry(self, entry):
        self.cursor.execute("""
            INSERT INTO entries (date, type, category, description, amount, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (entry.date, entry.type, entry.category, entry.description, entry.amount, entry.location))
        self.connection.commit()
        entry.id = self.cursor.lastrowid

    def get_expenses(self, branch=None):
        with self.connection:
            if branch:
                self.cursor.execute("SELECT * FROM entries WHERE type='EXPENSE' AND location=?", (branch,))
            else:
                self.cursor.execute("SELECT * FROM entries WHERE type='EXPENSE'")
            rows = self.cursor.fetchall()

        return [Entry(datetime.strptime(row[1], "%Y-%m-%d").date(), row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def get_revenues(self, branch=None):
        with self.connection:
            if branch:
                self.cursor.execute("SELECT * FROM entries WHERE type='REVENUE' AND location=?", (branch,))
            else:
                self.cursor.execute("SELECT * FROM entries WHERE type='REVENUE'")
            rows = self.cursor.fetchall()

        return [Entry(datetime.strptime(row[1], "%Y-%m-%d").date(), row[2], row[3], row[4], row[5], row[6]) for row in rows]

    def update_entry(self, entry):
        self.cursor.execute("""
            UPDATE entries
            SET date=?, type=?, category=?, description=?, amount=?, location=?
            WHERE id=?
        """, (entry.date, entry.type, entry.category, entry.description, entry.amount, entry.location, entry.id))
        self.connection.commit()

    def delete_entry(self, entry):
        self.cursor.execute("""
            DELETE FROM entries WHERE id=?                 
        """, (entry.id,))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
