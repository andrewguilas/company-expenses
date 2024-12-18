import tkinter as tk

class SumRow:
    def __init__(self, frame):
        self.build(frame)

    def build(self, frame):
        sum_row_frame = tk.Frame(frame)
        sum_row_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.sum_label = tk.Label(sum_row_frame, text="Total Amount: $0.00")
        self.sum_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.count_label = tk.Label(sum_row_frame, text="Total Entries: 0")
        self.count_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    def update(self, total_amount, entry_count):
        self.sum_label.config(text=f"Total Amount: ${total_amount:,.2f}")
        self.count_label.config(text=f"Total Entries: {entry_count}")
