import tkinter as tk
from tkinter import ttk
from managers.database import Database

def strip_string(string):
    return string.lower().strip().replace(" ", "").replace("_", "")

class EntriesScene:
    def __init__(self):
        self.database = Database()
        self.entries = []

    def build(self):
        self.frame = tk.Frame(self.root, name="entries_scene")

        self.search_label = tk.Label(self.frame, text="Search by column:")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_tree)

        self.tree = ttk.Treeview(self.frame, columns=("date", "category", "description", "amount", "location"), show="headings")
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("location", text="Location")
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.expenses_button = tk.Button(self.frame, text="Show Expenses", command=self.filter_by_expenses)
        self.expenses_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.revenues_button = tk.Button(self.frame, text="Show Revenues", command=self.filter_by_revenues)
        self.revenues_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Configure the row and column to expand with window resizing
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.filter_by_expenses()
        self.update_tree()

    def show(self, app):
        self.app = app
        self.root = app.root

        if not hasattr(self, "frame"):
            self.build()

        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def update_tree(self, event=None):
        search_query = self.search_entry.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for entry in self.entries:
            if self.meets_search_query(entry, search_query):
                self.tree.insert("", "end", values=(entry[1], entry[3], entry[4], entry[5], entry[6]))

    def meets_search_query(self, entry, search_query):
        return strip_string(search_query) in strip_string(str(entry))

    def filter_by_expenses(self):
        self.entries = self.database.get_expenses()
        self.update_tree()

    def filter_by_revenues(self):
        self.entries = self.database.get_revenues()
        self.update_tree()
