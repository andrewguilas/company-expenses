import tkinter as tk
from tkinter import ttk
from managers.database import Database

def strip_string(string):
    return string.lower().strip().replace(" ", "").replace("_", "")

def meets_search_query(entry, search_query):
     return strip_string(search_query) in strip_string(str(entry))

class EntriesScene:
    def __init__(self):
        self.database = Database()
        self.entries = []
        self.selected_location = None  # None represents "All Locations"
        self.selected_type = None  # None represents "All Types"
        self.selected_category = None  # None represents "All Categories"
        self.is_sorted_by = None  # No column is sorted by default
        self.sort_order = {}  # Stores the sort order for each column

    def build(self, root):
        self.frame = tk.Frame(root, name="entries_scene")

        self.build_search_bar()
        self.build_filter_row()
        self.build_tree()
        self.build_sum_row()

        # Configure row and column weights for resizing
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.update_tree()

    def build_search_bar(self):
        self.search_label = tk.Label(self.frame, text="Search by column:")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_tree)

    def build_filter_row(self):
        self.filter_frame = tk.Frame(self.frame)
        self.filter_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.locations = self.database.get_locations()
        self.location_filter_label = tk.Label(self.filter_frame, text="Filter by location:")
        self.location_filter_label.grid(row=0, column=0, padx=10, pady=5)
        self.location_filter = ttk.Combobox(self.filter_frame, values=["ALL"] + self.locations, state="readonly")
        self.location_filter.set("ALL")
        self.location_filter.grid(row=0, column=1, padx=10, pady=5)
        self.location_filter.bind("<<ComboboxSelected>>", self.update_tree)

        self.type_filter_label = tk.Label(self.filter_frame, text="Filter by type:")
        self.type_filter_label.grid(row=0, column=2, padx=10, pady=5)
        self.type_filter = ttk.Combobox(self.filter_frame, values=["ALL", "EXPENSE", "REVENUE"], state="readonly")
        self.type_filter.set("ALL")
        self.type_filter.grid(row=0, column=3, padx=10, pady=5)
        self.type_filter.bind("<<ComboboxSelected>>", self.update_tree)

        self.categories = self.database.get_categories()  # Assuming get_categories() returns all categories
        self.category_filter_label = tk.Label(self.filter_frame, text="Filter by category:")
        self.category_filter_label.grid(row=0, column=4, padx=10, pady=5)
        self.category_filter = ttk.Combobox(self.filter_frame, values=["ALL"] + self.categories, state="readonly")
        self.category_filter.set("ALL")
        self.category_filter.grid(row=0, column=5, padx=10, pady=5)
        self.category_filter.bind("<<ComboboxSelected>>", self.update_tree)

    def build_tree(self):
        self.tree = ttk.Treeview(self.frame, columns=("date", "type", "category", "description", "amount", "location"), show="headings")
        self.tree.heading("date", text="Date", command=lambda: self.sort_by_column("date"))
        self.tree.heading("type", text="Type", command=lambda: self.sort_by_column("type"))
        self.tree.heading("category", text="Category", command=lambda: self.sort_by_column("category"))
        self.tree.heading("description", text="Description", command=lambda: self.sort_by_column("description"))
        self.tree.heading("amount", text="Amount", command=lambda: self.sort_by_column("amount"))
        self.tree.heading("location", text="Location", command=lambda: self.sort_by_column("location"))
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def build_sum_row(self):
        self.sum_label = tk.Label(self.frame, text="Total Amount: $0.00")
        self.sum_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.count_label = tk.Label(self.frame, text="Total Entries: 0")
        self.count_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    def show(self, app):
        self.app = app

        if not hasattr(self, "frame"):
            self.build(app.root)

        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def update_tree(self, event=None):
        filtered_entries = self.database.get_expenses() + self.database.get_revenues()
        filtered_entries = self.apply_filters(filtered_entries)
        filtered_entries = self.apply_search(filtered_entries)
        filtered_entries = self.apply_sort(filtered_entries)

        self.clear_tree()

        total_amount = 0
        for entry in filtered_entries:
            date_str = entry.date.strftime("%m/%d/%Y")
            amount = entry.amount if entry.type == "REVENUE" else -entry.amount
            self.tree.insert("", "end", values=(date_str, entry.type, entry.category, entry.description, f"${amount:,.2f}", entry.location))
            total_amount += amount

        self.sum_label.config(text=f"Total Amount: ${total_amount:,.2f}")
        self.count_label.config(text=f"Total Entries: {len(filtered_entries)}")

    def apply_filters(self, filtered_entries):
        location_filter = self.location_filter.get()
        type_filter = self.type_filter.get()
        category_filter = self.category_filter.get()

        if location_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.location == location_filter]

        if type_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.type == type_filter]

        if category_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.category == category_filter]

        return filtered_entries

    def apply_search(self, filtered_entries):
        search_query = self.search_entry.get()
        filtered_entries = [entry for entry in filtered_entries if meets_search_query(entry, search_query)]
        return filtered_entries

    def apply_sort(self, filtered_entries):
        if self.is_sorted_by:
            filtered_entries = sorted(filtered_entries, key=lambda x: getattr(x, self.is_sorted_by), reverse=self.sort_order.get(self.is_sorted_by, True))
        return filtered_entries

    def clear_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def sort_by_column(self, column):
        if self.is_sorted_by == column:
            self.sort_order[column] = not self.sort_order.get(column, True)  # Reverse the order
        else:
            self.is_sorted_by = column
            self.sort_order[column] = True  # Default to ascending order

        self.update_tree()
