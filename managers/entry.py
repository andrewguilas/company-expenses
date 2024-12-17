class Entry():
    def __init__(self, date, type, category, description, amount, location):
        self.id = None
        self.date = date
        self.type = type # expense/revenue
        self.category = category
        self.description = description
        self.amount = amount
        self.location = location

    def __str__(self):
        return "{} {} {} {} {} {}".format(
            self.date,
            self.type,
            self.category,
            self.description,
            self.amount,
            self.location
        )
