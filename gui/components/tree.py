import tkinter as tk
from tkinter import ttk

class Tree:
    def __init__(self, parent, database):
        self.database = database
        self.entries = []  # List to store entries (expenses + revenues)
        self.is_sorted_by = None  # No column is sorted by default
        self.sort_order = {}  # Store sort order for each column
        
        # Treeview setup
        self.tree = ttk.Treeview(parent, columns=("date", "type", "category", "description", "amount", "location"), show="headings")
        self.tree.heading("date", text="Date", command=lambda: self.sort_by_column("date"))
        self.tree.heading("type", text="Type", command=lambda: self.sort_by_column("type"))
        self.tree.heading("category", text="Category", command=lambda: self.sort_by_column("category"))
        self.tree.heading("description", text="Description", command=lambda: self.sort_by_column("description"))
        self.tree.heading("amount", text="Amount", command=lambda: self.sort_by_column("amount"))
        self.tree.heading("location", text="Location", command=lambda: self.sort_by_column("location"))
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def sort_by_column(self, column):
        # Toggle the sort order: if already sorted by this column, reverse the order
        if self.is_sorted_by == column:
            self.sort_order[column] = not self.sort_order.get(column, True)  # Reverse the order
        else:
            self.is_sorted_by = column
            self.sort_order[column] = True  # Default to ascending order

        # Apply sorting after changing the sort order
        self.update_tree()

    def update_tree(self):
        # Fetch all entries from database
        filtered_entries = self.database.get_expenses() + self.database.get_revenues()
        
        # Apply sorting to the filtered entries
        filtered_entries = self.apply_sort(filtered_entries)
        
        # Clear the tree before updating
        self.clear_tree()

        # Insert sorted entries into the tree view
        for entry in filtered_entries:
            date_str = entry.date.strftime("%m/%d/%Y")
            amount = entry.amount if entry.type == "REVENUE" else -entry.amount
            self.tree.insert("", "end", values=(date_str, entry.type, entry.category, entry.description, f"${amount:,.2f}", entry.location))

    def apply_sort(self, filtered_entries):
        if self.is_sorted_by:
            filtered_entries = sorted(
                filtered_entries,
                key=lambda x: getattr(x, self.is_sorted_by),
                reverse=self.sort_order.get(self.is_sorted_by, True)  # Reverse if required
            )
        return filtered_entries

    def clear_tree(self):
        # Clear all rows in the tree
        for row in self.tree.get_children():
            self.tree.delete(row)
