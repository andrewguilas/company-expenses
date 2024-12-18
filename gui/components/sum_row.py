import tkinter as tk

class SumRow:
    def __init__(self, frame):
        self.frame = frame
        self.build_widgets()

    def build_widgets(self):
        self.sum_label = tk.Label(self.frame, text="Total Amount: $0.00")
        self.sum_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.count_label = tk.Label(self.frame, text="Total Entries: 0")
        self.count_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    def update(self, total_amount, entry_count):
        self.sum_label.config(text=f"Total Amount: ${total_amount:,.2f}")
        self.count_label.config(text=f"Total Entries: {entry_count}")
