import tkinter as tk
from .filter_row import FilterRow
from .search_bar import SearchBar
from .tree import Tree
from .sum_row import SumRow
from .upload_button import UploadButton
from managers.database import Database

class EntriesScene:
    def __init__(self):
        self.database = Database()

    def build(self, root):
        self.frame = tk.Frame(root, name="entries_scene")
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.sum_row = SumRow(self.frame)
        self.tree = Tree(self.frame, self.database, self.sum_row)
        self.search_bar = SearchBar(self.frame, self.tree)
        self.filter_row = FilterRow(self.frame, self.database, self.tree)
        self.upload_button = UploadButton(self.frame, self.database, self.filter_row.update_filter_options, self.tree.update_tree)

        self.summary_button = tk.Button(self.frame, text="Summary", command=self.show_summary_scene)
        self.summary_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=0)
        self.frame.grid_columnconfigure(0, weight=1)

        self.tree.update_tree()

    def show(self, app):
        self.app = app
        if not hasattr(self, "frame"):
            self.build(app.root)
        self.frame.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        self.frame.grid_forget()

    def show_summary_scene(self):
        self.hide()
        self.app.show_summary_scene()
