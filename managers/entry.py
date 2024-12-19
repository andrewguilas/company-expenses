from enum import Enum

class EntryType(Enum):
    EXPENSE = "EXPENSE"
    REVENUE = "REVENUE"

class Entry:
    def __init__(self, date, type, category, description, amount, location, id=None):
        self.id = id
        self.date = date
        self.type = type
        self.category = category
        self.description = description
        self.amount = amount
        self.location = location

    def __str__(self):
        return f"{self.date.strftime('%m/%d/%Y')} {self.type} {self.category} {self.description} {self.amount} {self.location}"

    def __repr__(self):
        return f"Entry(id={self.id}, date={self.date}, type={self.type}, category={self.category}, description={self.description}, amount={self.amount}, location={self.location})"

