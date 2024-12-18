import tkinter as tk
from managers.database import Database

class SummaryScene:
    def __init__(self):
        self.database = Database()

    def build(self, root):
        self.frame = tk.Frame(root, name="summary_scene")
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.summary_button = tk.Button(self.frame, text="Entries", command=self.show_entries_scene)
        self.summary_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def show(self, app):
        self.app = app
        if not hasattr(self, "frame"):
            self.build(app.root)
        self.frame.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        self.frame.grid_forget()

    def show_entries_scene(self, event=None):
        self.hide()
        self.app.show_entries_scene()
