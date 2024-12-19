import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
from datetime import datetime
from . import csv_parser
from managers.database import DuplicateEntryError
from managers.entry import Entry, EntryType

class UploadButton:
    def __init__(self, frame, database, update_filter_options, update_tree):
        self.database = database
        self.update_filter_options = update_filter_options
        self.update_tree = update_tree

        self.build(frame)

    def build(self, frame):
        self.upload_button = tk.Button(frame, text="Upload data (.csv)", command=self.request_csv)
        self.upload_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    def request_csv(self):
        self.upload_button.config(state="disabled")
        file = filedialog.askopenfile(mode='r', initialdir=os.getcwd(), filetypes=[("CSV Files", "*.csv")])

        if file is None:
            self.upload_button.config(state="normal")
            return  # User canceled the dialog

        try:
            rows = self.get_data_from_csv(file)

            entries, invalid_rows = [], []
            if "2019" in file.name:
                entries, invalid_rows = csv_parser.convert_row_to_entry_2019(rows)
            elif "2023" in file.name:
                entries, invalid_rows = csv_parser.convert_row_to_entry_2023(rows)

            if invalid_rows:
                raise ValueError(f"{len(invalid_rows)} invalid rows were found and ignored")

            duplicate_rows = []
            for entry in entries:
                try:
                    self.database.add_entry(entry)
                except DuplicateEntryError as error_message:
                    duplicate_rows.append(error_message)

            if len(duplicate_rows) > 0:
                raise ValueError(f"{len(duplicate_rows)} duplicate rows were found and ignored")

            self.update_filter_options()
            self.update_tree()
        except Exception as error_message:
            messagebox.showerror("Error", f"Failed to process CSV file:\n{error_message}")
        finally:
            print("done")
            file.close()
            self.upload_button.config(state="normal")
            print("done2")

    def get_data_from_csv(self, file):
        reader = csv.reader(file)
        data = list(reader)
        if not data:
            raise ValueError("The selected file is missing required columns.")

        return data[1:]  # Remove heading row
