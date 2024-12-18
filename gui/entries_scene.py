import tkinter as tk
from gui.components.filter_row import FilterRow
from gui.components.search_bar import SearchBar
from gui.components.tree import Tree
from gui.components.sum_row import SumRow
from gui.components.upload_button import UploadButton
from managers.database import Database

class EntriesScene:
    def __init__(self):
        self.database = Database()

    def build(self, root):
        self.frame = tk.Frame(root, name="entries_scene")

        self.sum_row = SumRow(self.frame)
        self.tree = Tree(self.frame, self.database, self.sum_row)
        self.search_bar = SearchBar(self.frame, self.tree)
        self.filter_row = FilterRow(self.frame, self.database, self.tree)
        self.upload_button = UploadButton(self.frame, self.database, self.filter_row.update_filter_options, self.tree.update_tree)

        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.tree.update_tree()

    def show(self, app):
        self.app = app

        if not hasattr(self, "frame"):
            self.build(app.root)

        self.frame.grid(row=0, column=0, sticky="nsew")


    def hide(self):
        self.frame.pack_forget()
