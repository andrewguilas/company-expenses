import tkinter as tk
from gui.components.filter_row import FilterRow
from gui.components.search_bar import SearchBar
from gui.components.tree import Tree
from gui.components.sum_row import SumRow
from managers.database import Database

def strip_string(string):
    return string.lower().strip().replace(" ", "").replace("_", "")

def meets_search_query(entry, search_query):
     return strip_string(search_query) in strip_string(str(entry))

class EntriesScene:
    def __init__(self):
        self.database = Database()
        self.entries = []
        self.selected_location = None
        self.selected_type = None
        self.selected_category = None
        self.is_sorted_by = None
        self.sort_order = {}

    def build(self, root):
        self.frame = tk.Frame(root, name="entries_scene")

        self.search_bar = SearchBar(self.frame, self.update_tree)
        self.filter_row = FilterRow(self.frame, self.database, self.update_tree)
        self.tree = Tree(self.frame, self.database)
        self.sum_row = SumRow(self.frame)

        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.update_tree()

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

        self.tree.clear_tree()

        total_amount = 0
        for entry in filtered_entries:
            date_str = entry.date.strftime("%m/%d/%Y")
            amount = entry.amount if entry.type == "REVENUE" else -entry.amount
            self.tree.tree.insert("", "end", values=(date_str, entry.type, entry.category, entry.description, f"${amount:,.2f}", entry.location))
            total_amount += amount

        self.sum_row.update(total_amount, len(filtered_entries))

    def apply_filters(self, filtered_entries):
        location_filter = self.filter_row.location_filter.get()
        type_filter = self.filter_row.type_filter.get()
        category_filter = self.filter_row.category_filter.get()

        if location_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.location == location_filter]

        if type_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.type == type_filter]

        if category_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.category == category_filter]

        return filtered_entries

    def apply_search(self, filtered_entries):
        search_query = self.search_bar.search_entry.get()
        filtered_entries = [entry for entry in filtered_entries if meets_search_query(entry, search_query)]
        return filtered_entries

    def apply_sort(self, filtered_entries):
        if self.is_sorted_by:
            filtered_entries = sorted(filtered_entries, key=lambda x: getattr(x, self.is_sorted_by), reverse=self.sort_order.get(self.is_sorted_by, True))
        return filtered_entries
