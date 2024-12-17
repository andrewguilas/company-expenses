import csv
import datetime
import tkinter
from tkinter import filedialog
import os
import tkinter.messagebox
from datetime import datetime
from managers.database import Database
from managers.entry import Entry   

def convert_string_to_date(date_string):
    return datetime.strptime(date_string, "%m/%d/%Y").date()

def convert_string_to_amount(amount_string):
    cleaned_string = amount_string.replace(",", "")
    if "(" in cleaned_string and ")" in cleaned_string: # () mean negative
        amount = float(cleaned_string.replace("(", "-").replace(")", "").replace("$", ""))
    else:
        amount = float(cleaned_string.replace("$", ""))
    return amount

def check_for_missing_data(data):
    return [value for value in data if value is None]

class UploadScene():
    def __init__(self):
        self.database = Database()

    def build(self):
        self.frame = tkinter.Frame(self.root, name="upload_scene")
        self.upload_button = tkinter.Button(self.frame, text="Upload data (.csv)", command=self.request_csv)
        self.upload_button.grid()

    def show(self, app):
        self.app = app
        self.root = app.root

        if not hasattr(self, "frame"):
            self.build()

        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def request_csv(self, event=None):
        file = filedialog.askopenfile(mode='r', initialdir=os.getcwd(), filetypes=[("CSV Files", "*.csv")])
        if file is None:
            return # user canceled dialogue
        
        try:
            rows = self.get_data_from_csv(file)
            entries = self.convert_row_to_entry(rows)
            for entry in entries:
                self.database.add_entry(entry)
        except Exception as error_message:
            tkinter.messagebox.showerror("Error", f"Failed to process csv file:\n{error_message}")
        finally:
            file.close()
    
    def get_data_from_csv(self, file):
        reader = csv.reader(file)
        data = list(reader)
        if not data:
            raise ValueError("The selected file is empty")
        
        return data[1:] # remove heading row

    def convert_row_to_entry(self, rows):
        entries = []
        for row in rows:
            date = row[0]
            category = row[1].upper()
            description = row[2].upper()
            amount = row[3]
            location = row[4].upper()

            missing_data = check_for_missing_data([date, category, description, amount, location])
            if missing_data:
                raise ValueError(f"Missing required data: {', '.join(missing_data)}")

            try:
                date = convert_string_to_date(date)
            except Exception as error_message:
                raise ValueError(f"Date is not in valid date format mm/dd/yyyy\n{error_message}")
            
            try:
                amount = convert_string_to_amount(amount)
            except Exception as error_message:
                raise ValueError(f"Amount is not in valid accounting format $(xxx.xx)\n{error_message}")
                
            type = amount < 0 and "EXPENSE" or "REVENUE"
            amount=abs(amount)

            entries.append(Entry(date, type, category, description, amount, location)) 

        return entries
    