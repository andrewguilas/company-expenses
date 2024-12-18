import tkinter as tk
from tkinter import ttk

class FilterRow:
    def __init__(self, frame, database, update_callback):
        self.database = database
        self.update_callback = update_callback
        self.frame = tk.Frame(frame)
        self.frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.build_widgets()

    def build_widgets(self):
        self.locations = self.database.get_locations()
        self.location_filter_label = tk.Label(self.frame, text="Filter by location:")
        self.location_filter_label.grid(row=0, column=0, padx=10, pady=5)
        self.location_filter = ttk.Combobox(self.frame, values=["ALL"] + self.locations, state="readonly")
        self.location_filter.set("ALL")
        self.location_filter.grid(row=0, column=1, padx=10, pady=5)
        self.location_filter.bind("<<ComboboxSelected>>", self.update_callback)

        self.type_filter_label = tk.Label(self.frame, text="Filter by type:")
        self.type_filter_label.grid(row=0, column=2, padx=10, pady=5)
        self.type_filter = ttk.Combobox(self.frame, values=["ALL", "EXPENSE", "REVENUE"], state="readonly")
        self.type_filter.set("ALL")
        self.type_filter.grid(row=0, column=3, padx=10, pady=5)
        self.type_filter.bind("<<ComboboxSelected>>", self.update_callback)

        self.categories = self.database.get_categories()
        self.category_filter_label = tk.Label(self.frame, text="Filter by category:")
        self.category_filter_label.grid(row=0, column=4, padx=10, pady=5)
        self.category_filter = ttk.Combobox(self.frame, values=["ALL"] + self.categories, state="readonly")
        self.category_filter.set("ALL")
        self.category_filter.grid(row=0, column=5, padx=10, pady=5)
        self.category_filter.bind("<<ComboboxSelected>>", self.update_callback)
