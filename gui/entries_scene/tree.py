from tkinter import ttk

def strip_string(string):
    return string.lower().strip().replace(" ", "").replace("_", "")

def meets_search_query(entry, search_query):
    return strip_string(search_query) in strip_string(str(entry))

class Tree:
    def __init__(self, frame, database, sum_row):
        self.database = database
        self.sum_row = sum_row
        self.entries = []

        self.search_query = ""
        self.selected_location = None  # If none, then selected location is all
        self.selected_type = None  # If none, then selected type is all
        self.selected_category = None  # if none, then selected category is all
        self.is_sorted_by = None  # No column is sorted by default
        self.sort_order = {}  # Store sort order for each column

        self.build(frame)

    def build(self, frame):
        self.tree = ttk.Treeview(frame, columns=("date", "type", "category", "description", "amount", "location"), show="headings")
        self.tree.heading("date", text="Date", command=lambda: self.update_sorted_by("date"))
        self.tree.heading("type", text="Type", command=lambda: self.update_sorted_by("type"))
        self.tree.heading("category", text="Category", command=lambda: self.update_sorted_by("category"))
        self.tree.heading("description", text="Description", command=lambda: self.update_sorted_by("description"))
        self.tree.heading("amount", text="Amount", command=lambda: self.update_sorted_by("amount"))
        self.tree.heading("location", text="Location", command=lambda: self.update_sorted_by("location"))
        self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def update_sorted_by(self, column):
        # Toggle the sort order: if already sorted by this column, reverse the order
        if self.is_sorted_by == column:
            self.sort_order[column] = not self.sort_order.get(column, True)  # Reverse the order
        else:
            self.is_sorted_by = column
            self.sort_order[column] = True  # Default to ascending order

        self.update_tree()

    def update_tree(self, search_query=None, selected_location=None, selected_type=None, selected_category=None):
        if search_query is not None:
            self.search_query = search_query

        if selected_location is not None:
            self.selected_location = selected_location

        if selected_type is not None:
            self.selected_type = selected_type

        if selected_category is not None:
            self.selected_category = selected_category

        # sort order is already set in the above update_sorted_by()

        filtered_entries = self.database.get_expenses() + self.database.get_revenues()
        filtered_entries = self.apply_filters(filtered_entries)
        filtered_entries = self.apply_search(filtered_entries)
        filtered_entries = self.apply_sort(filtered_entries)

        self.clear_tree()

        total_amount = 0
        for entry in filtered_entries:
            date_str = entry.date.strftime("%m/%d/%Y")
            self.tree.insert("", "end", values=(date_str, entry.type, entry.category, entry.description, f"${entry.amount:,.2f}", entry.location))
            total_amount += entry.amount

        self.sum_row.update(total_amount, len(filtered_entries))

    def apply_filters(self, filtered_entries):
        location_filter = self.selected_location if self.selected_location else "ALL"
        type_filter = self.selected_type if self.selected_type else "ALL"
        category_filter = self.selected_category if self.selected_category else "ALL"

        if location_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.location == location_filter]

        if type_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.type == type_filter]

        if category_filter != "ALL":
            filtered_entries = [entry for entry in filtered_entries if entry.category == category_filter]

        return filtered_entries

    def apply_search(self, filtered_entries):
        return [entry for entry in filtered_entries if meets_search_query(entry, self.search_query)]

    def apply_sort(self, filtered_entries):
        if self.is_sorted_by:
            filtered_entries = sorted(filtered_entries, key=lambda x: getattr(x, self.is_sorted_by), reverse=self.sort_order.get(self.is_sorted_by, True))
        return filtered_entries

    def clear_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
