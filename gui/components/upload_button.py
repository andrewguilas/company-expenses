import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
from datetime import datetime
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
            return  # User canceled the dialog

        try:
            rows = self.get_data_from_csv(file)
            entries, invalid_rows = self.convert_row_to_entry(rows)

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
            file.close()
            self.upload_button.config(state="normal")

    def get_data_from_csv(self, file):
        reader = csv.reader(file)
        data = list(reader)
        if not data or len(data[0]) < 5:
            raise ValueError("The selected file is missing required columns.")

        return data[1:]  # Remove heading row

    def convert_row_to_entry(self, rows):
        entries = []
        invalid_rows = []
        for row_idx, row in enumerate(rows, start=2):  # Start at row 2 to indicate the actual row number
            try:
                missing_data = self.check_for_missing_data(row)
                if missing_data:
                    raise ValueError(f"Missing data in row {row_idx}: {missing_data}")

                date = self.convert_string_to_date(row[0])
                amount = self.convert_string_to_amount(row[3])
                entry_type = EntryType.EXPENSE if amount < 0 else EntryType.REVENUE
                entries.append(Entry(date, entry_type, row[1].upper(), row[2].upper(), amount, row[4].upper()))
            except Exception as error_message:
                invalid_rows.append(f"Row {row_idx}: {error_message}")
                continue

        return entries, invalid_rows

    def convert_string_to_date(self, date_string):
        try:
            return datetime.strptime(date_string, "%m/%d/%Y").date()
        except ValueError:
            raise ValueError(f"Invalid date format: {date_string}. Expected MM/DD/YYYY.")

    def convert_string_to_amount(self, amount_string):
        try:
            cleaned_string = amount_string.replace(",", "")
            if "(" in cleaned_string and ")" in cleaned_string:  # () in account form means negative
                amount = float(cleaned_string.replace("(", "-").replace(")", "").replace("$", ""))
            else:
                amount = float(cleaned_string.replace("$", ""))
            return amount
        except ValueError:
            raise ValueError(f"Invalid amount format: {amount_string}. Expected numeric or formatted amount.")

    def check_for_missing_data(self, data):
        missing_indices = []
        for idx, value in enumerate(data):
            if idx <= 4 and not value.strip():
                missing_indices.append(idx)
        return missing_indices
