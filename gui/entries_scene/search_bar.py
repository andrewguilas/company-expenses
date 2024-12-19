import tkinter as tk

class SearchBar:
    def __init__(self, frame, tree):
        self.tree = tree
        self.build(frame)

    def build(self, frame):
        search_bar_frame = tk.Frame(frame)
        search_bar_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.search_label = tk.Label(search_bar_frame, text="Search by column:")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(search_bar_frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_search_query)

    def update_search_query(self, event=None):
        search_query = self.search_entry.get()
        self.tree.update_tree(search_query=search_query)
