class Entry:
    def __init__(self, date, type, category, description, amount, location):
        self.id = None
        self.date = date
        self.type = type  # 'EXPENSE' or 'REVENUE'
        self.category = category
        self.description = description
        self.amount = amount
        self.location = location

    def __str__(self):
        return f"{self.date.strftime('%m/%d/%Y')} {self.type} {self.category} {self.description} {self.amount} {self.location}"
