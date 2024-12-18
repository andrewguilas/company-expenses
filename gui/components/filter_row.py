import tkinter as tk
from tkinter import ttk

class FilterRow:
    def __init__(self, frame, database, tree):
        self.database = database
        self.tree = tree
        self.locations = self.database.get_locations()
        self.categories = self.database.get_categories()

        self.build(frame)

    def build(self, frame):
        filter_row_frame = tk.Frame(frame)
        filter_row_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.build_location_filter(filter_row_frame)
        self.build_type_filter(filter_row_frame)
        self.build_category_filter(filter_row_frame)

    def build_location_filter(self, filter_row_frame):
        location_filter_label = tk.Label(filter_row_frame, text="Filter by location:")
        location_filter_label.grid(row=0, column=0, padx=10, pady=5)

        self.location_filter = ttk.Combobox(filter_row_frame, values=["ALL"] + self.locations, state="readonly")
        self.location_filter.set("ALL")
        self.location_filter.grid(row=0, column=1, padx=10, pady=5)
        self.location_filter.bind("<<ComboboxSelected>>", self.update_selected_filters)

    def build_type_filter(self, filter_row_frame):
        type_filter_label = tk.Label(filter_row_frame, text="Filter by type:")
        type_filter_label.grid(row=0, column=2, padx=10, pady=5)

        self.type_filter = ttk.Combobox(filter_row_frame, values=["ALL", "EXPENSE", "REVENUE"], state="readonly")
        self.type_filter.set("ALL")
        self.type_filter.grid(row=0, column=3, padx=10, pady=5)
        self.type_filter.bind("<<ComboboxSelected>>", self.update_selected_filters)

    def build_category_filter(self, filter_row_frame):
        category_filter_label = tk.Label(filter_row_frame, text="Filter by category:")
        category_filter_label.grid(row=0, column=4, padx=10, pady=5)

        self.category_filter = ttk.Combobox(filter_row_frame, values=["ALL"] + self.categories, state="readonly")
        self.category_filter.set("ALL")
        self.category_filter.grid(row=0, column=5, padx=10, pady=5)
        self.category_filter.bind("<<ComboboxSelected>>", self.update_selected_filters)

    def update_filter_options(self):
        self.locations = self.database.get_locations()
        self.categories = self.database.get_categories()

        self.location_filter['values'] = ["ALL"] + self.locations
        self.location_filter.set("ALL")

        self.category_filter['values'] = ["ALL"] + self.categories
        self.category_filter.set("ALL")

    def update_selected_filters(self, event=None):
        selected_location = self.location_filter.get()
        selected_type = self.type_filter.get()
        selected_category = self.category_filter.get()
        self.tree.update_tree(selected_location=selected_location, selected_type=selected_type, selected_category=selected_category)
