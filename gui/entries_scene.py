import tkinter as tk
from tkinter import ttk
from managers.database import Database

def strip_string(string):
    return string.lower().strip().replace(" ", "").replace("_", "")

class EntriesScene:
    def __init__(self):
        self.database = Database()
        self.entries = []
        self.locations = self.database.get_locations()
        self.categories = self.database.get_categories()  # Assuming get_categories() returns all categories
        self.selected_location = None  # None represents "All Locations"
        self.selected_type = None  # None represents "All Types"
        self.selected_category = None  # None represents "All Categories"
        self.is_sorted_by = None  # No column is sorted by default
        self.sort_order = {}  # Dictionary to store the sort order for each column

    def build(self):
        self.frame = tk.Frame(self.root, name="entries_scene")

        # Search box
        self.search_label = tk.Label(self.frame, text="Search by column:")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_tree)

        # Filter row (location, type, category)
        self.filter_frame = tk.Frame(self.frame)
        self.filter_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Location filter
        self.location_filter_label = tk.Label(self.filter_frame, text="Filter by location:")
        self.location_filter_label.grid(row=0, column=0, padx=10, pady=5)
        self.location_filter = ttk.Combobox(self.filter_frame, values=["ALL"] + self.locations, state="readonly")
        self.location_filter.set("ALL")
        self.location_filter.grid(row=0, column=1, padx=10, pady=5)
        self.location_filter.bind("<<ComboboxSelected>>", self.update_tree)

        # Type filter
        self.type_filter_label = tk.Label(self.filter_frame, text="Filter by type:")
        self.type_filter_label.grid(row=0, column=2, padx=10, pady=5)
        self.type_filter = ttk.Combobox(self.filter_frame, values=["ALL", "EXPENSE", "REVENUE"], state="readonly")
        self.type_filter.set("ALL")
        self.type_filter.grid(row=0, column=3, padx=10, pady=5)
        self.type_filter.bind("<<ComboboxSelected>>", self.update_tree)

        # Category filter
        self.category_filter_label = tk.Label(self.filter_frame, text="Filter by category:")
        self.category_filter_label.grid(row=0, column=4, padx=10, pady=5)
        self.category_filter = ttk.Combobox(self.filter_frame, values=["ALL"] + self.categories, state="readonly")
        self.category_filter.set("ALL")
        self.category_filter.grid(row=0, column=5, padx=10, pady=5)
        self.category_filter.bind("<<ComboboxSelected>>", self.update_tree)

        # Treeview for entries
        self.tree = ttk.Treeview(self.frame, columns=("date", "type", "category", "description", "amount", "location"), show="headings")
        self.tree.heading("date", text="Date", command=lambda: self.sort_by_column("date"))
        self.tree.heading("type", text="Type", command=lambda: self.sort_by_column("type"))
        self.tree.heading("category", text="Category", command=lambda: self.sort_by_column("category"))
        self.tree.heading("description", text="Description", command=lambda: self.sort_by_column("description"))
        self.tree.heading("amount", text="Amount", command=lambda: self.sort_by_column("amount"))
        self.tree.heading("location", text="Location", command=lambda: self.sort_by_column("location"))
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configure row and column weights for resizing
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Labels for sum and count
        self.sum_label = tk.Label(self.frame, text="Total Amount: $0.00")
        self.sum_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.count_label = tk.Label(self.frame, text="Total Entries: 0")
        self.count_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

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
        location_filter = self.location_filter.get()
        type_filter = self.type_filter.get()
        category_filter = self.category_filter.get()

        # Apply filters
        filtered_entries = self.database.get_expenses() + self.database.get_revenues()

        if location_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.location == location_filter]

        if type_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.type == type_filter]

        if category_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.category == category_filter]

        # Apply search filter
        filtered_entries = [entry for entry in filtered_entries if self.meets_search_query(entry, search_query)]

        # Apply sorting
        if self.is_sorted_by:
            filtered_entries = sorted(filtered_entries, key=lambda x: getattr(x, self.is_sorted_by), reverse=self.sort_order.get(self.is_sorted_by, True))

        # Clear existing entries in the tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert filtered and sorted entries into the tree
        total_amount = 0
        for entry in filtered_entries:
            date_str = entry.date.strftime("%m/%d/%Y")
            
            # Set amount to negative for expenses, positive for revenues
            amount = entry.amount if entry.type == "REVENUE" else -entry.amount

            self.tree.insert("", "end", values=(date_str, entry.type, entry.category, entry.description, f"${amount:,.2f}", entry.location))
            total_amount += amount

        # Update sum and count labels
        self.sum_label.config(text=f"Total Amount: ${total_amount:,.2f}")
        self.count_label.config(text=f"Total Entries: {len(filtered_entries)}")

    def meets_search_query(self, entry, search_query):
        return strip_string(search_query) in strip_string(str(entry))

    def sort_by_column(self, column):
        # Toggle the sort order for the clicked column
        if self.is_sorted_by == column:
            self.sort_order[column] = not self.sort_order.get(column, True)  # Reverse the order
        else:
            self.is_sorted_by = column
            self.sort_order[column] = True  # Default to ascending order

        # Re-sort and update the treeview
        self.update_tree()
