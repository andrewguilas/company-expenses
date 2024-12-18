import tkinter as tk

class SearchBar:
    def __init__(self, frame, update_callback):
        self.frame = frame
        self.update_callback = update_callback
        self.build_widgets()

    def build_widgets(self):
        self.search_label = tk.Label(self.frame, text="Search by column:")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.update_callback)
