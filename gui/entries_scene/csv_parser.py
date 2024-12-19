from datetime import datetime
from managers.entry import Entry, EntryType

def convert_row_to_entry_old(rows):
    entries = []
    invalid_rows = []
    for row_idx, row in enumerate(rows, start=2):  # Start at row 2 to indicate the actual row number
        try:
            missing_data = check_for_missing_data(row, 3)
            if missing_data:
                raise ValueError(f"Missing data in row {row_idx}: {missing_data}")

            date = convert_string_to_date(row[0])
            description_parts = row[1].split("_", 3)
            category = description_parts[0]
            description = description_parts[2]
            amount = convert_string_to_amount(row[2])
            location = description_parts[1]
            entry_type = EntryType.EXPENSE if amount < 0 else EntryType.REVENUE
            entries.append(Entry(date, entry_type, category, description, amount, location))
        except Exception as error_message:
            invalid_rows.append(f"Row {row_idx}: {error_message}")
            continue

    return entries, invalid_rows

def convert_row_to_entry_new(rows):
    entries = []
    invalid_rows = []
    for row_idx, row in enumerate(rows, start=2):  # Start at row 2 to indicate the actual row number
        try:
            missing_data = check_for_missing_data(row, 4)
            if missing_data:
                raise ValueError(f"Missing data in row {row_idx}: {missing_data}")

            date = convert_string_to_date(row[0])
            amount = convert_string_to_amount(row[3])
            entry_type = EntryType.EXPENSE if amount < 0 else EntryType.REVENUE
            entries.append(Entry(date, entry_type, row[1].upper(), row[2].upper(), amount, row[4].upper()))
        except Exception as error_message:
            invalid_rows.append(f"Row {row_idx}: {error_message}")
            continue

    return entries, invalid_rows

def convert_string_to_date(date_string):
    try:
        return datetime.strptime(date_string, "%m/%d/%Y").date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}. Expected MM/DD/YYYY.")

def convert_string_to_amount(amount_string):
    try:
        cleaned_string = amount_string.replace(",", "").replace("$", "").replace("(", "-").replace(")", "")
        return float(cleaned_string)
    except ValueError:
        raise ValueError(f"Invalid amount format: {amount_string}. Expected numeric or formatted amount.")

def check_for_missing_data(data, max_columns):
    missing_indices = []
    for idx, value in enumerate(data):
        if idx <= max_columns and not value.strip():
            missing_indices.append(idx)
    return missing_indices
