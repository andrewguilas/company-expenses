import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from dateutil.relativedelta import relativedelta  # Added for month handling
from managers.database import Database

class SummaryScene:
    def __init__(self):
        self.database = Database()

    def build(self, root):
        self.frame = tk.Frame(root, name="summary_scene", bg="white")
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.category_label = tk.Label(self.frame, text="Select Category:", bg="white")
        self.category_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.category_dropdown = ttk.Combobox(self.frame, state="readonly")
        self.category_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_charts)

        self.canvas_frame = tk.Frame(self.frame, bg="white")
        self.canvas_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chart_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.chart_frame, anchor="nw")

        self.entries_button = tk.Button(self.frame, text="Entries", command=self.show_entries_scene, bg="white")
        self.entries_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(0, weight=1)

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

    def show(self, app):
        self.app = app
        if not hasattr(self, "frame"):
            self.build(app.root)
        self.frame.grid(row=0, column=0, sticky="nsew")

        categories = self.database.get_categories()
        self.category_dropdown["values"] = categories

        self.update_charts()

    def hide(self):
        self.frame.grid_forget()

    def get_stats(self):
        stats = {}
        entries = self.database.get_entries()        
        for entry in entries:
            if entry.location not in stats:
                stats[entry.location] = {}

            if entry.category not in stats[entry.location]:
                stats[entry.location][entry.category] = {}

            # Initialize the months for each category-location pair
            for year in [2022, 2023]:
                for month in range(1, 13):
                    date_string = f"{year}_{month:02d}"  # Zero-padded months
                    if date_string not in stats[entry.location][entry.category]:
                        stats[entry.location][entry.category][date_string] = {
                            "YEAR": year,
                            "MONTH": month,
                            "COUNT": 0,
                            "AMOUNT": 0
                        }


            date_string = f"{entry.date.year}_{entry.date.month:02d}"
            # Ensure the key exists before updating
            if date_string not in stats[entry.location][entry.category]:
                stats[entry.location][entry.category][date_string] = {
                    "YEAR": entry.date.year,
                    "MONTH": entry.date.month,
                    "COUNT": 0,
                    "AMOUNT": 0
                }

            stats[entry.location][entry.category][date_string]["COUNT"] += 1
            stats[entry.location][entry.category][date_string]["AMOUNT"] += entry.amount

        return stats

    def update_charts(self, event=None):
        selected_category = self.category_dropdown.get()
        if not selected_category:
            return

        self.clear_charts()
        stats = self.get_stats()

        # Collect all locations to determine the number of histograms
        locations = [location for location in stats]
        num_locations = len(locations)

        # Dynamic figure height adjustment
        total_canvas_height = 600  # Total height available for all histograms
        histogram_height = total_canvas_height / num_locations  # Height for each histogram

        # Create a single figure with multiple subplots
        fig, axes = plt.subplots(
            num_locations, 1, figsize=(10, total_canvas_height / 100),
            sharex=True, constrained_layout=True
        )
        if num_locations == 1:
            axes = [axes]  # Ensure axes is always a list for uniform handling

        for ax, location in zip(axes, locations):
            for category, data in stats[location].items():
                if category == selected_category:
                    self.display_histogram(ax, category, data, location)

        # Add a unified X-axis on the bottom-most subplot
        self.add_shared_xaxis(axes[-1])

        # Center the charts on the screen
        fig.patch.set_facecolor('white')
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=50, padx=10, fill=tk.BOTH, expand=True)  # Add padding for centering

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def display_histogram(self, ax, category, data, location):
        MIN_DATE = "2022_1"
        MAX_DATE = "2023_12"

        # Define the range of months to include all months even with no data
        start_date = datetime.strptime(MIN_DATE, "%Y_%m")
        end_date = datetime.strptime(MAX_DATE, "%Y_%m")

        # Generate a list of months between start_date and end_date
        months = []
        current_date = start_date
        while current_date <= end_date:
            months.append(current_date.strftime("%Y_%m"))
            current_date += relativedelta(months=1)

        # Initialize the full data dictionary with zero amounts for missing months
        full_data = {month: 0 for month in months}
        for month_year, values in data.items():
            if month_year in full_data:
                full_data[month_year] = abs(values["AMOUNT"])  # Use absolute value for amounts

        # Extract amounts in the correct order of months
        amounts = [full_data[month] for month in months]

        # Plot the histogram
        ax.bar(range(len(months)), amounts, color="skyblue", edgecolor="black")

        # Add location title inside the chart
        ax.text(
            0.01, 0.95, location, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='left', color='black', weight='bold'
        )

        # Remove chart border and grid for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('gray')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)

    def add_shared_xaxis(self, ax):
        MIN_DATE = "2022_1"
        MAX_DATE = "2023_12"

        # Define the range of months to include all months even with no data
        start_date = datetime.strptime(MIN_DATE, "%Y_%m")
        end_date = datetime.strptime(MAX_DATE, "%Y_%m")

        months = []
        month_labels = []
        current_year = None
        year_positions = []  # To store the middle positions for years
        year_labels = []

        current_date = start_date
        index = 0

        while current_date <= end_date:
            months.append(current_date.strftime("%Y_%m"))
            month_labels.append(current_date.strftime("%b")[0])  # First letter of the month

            # If the year changes, compute the midpoint for the previous year
            if current_year != current_date.year:
                if current_year is not None:
                    middle_index = index - 6  # June/July is approximately 6 months back
                    year_positions.append(middle_index)
                    year_labels.append(current_year)

                current_year = current_date.year

            current_date += relativedelta(months=1)
            index += 1

        # Add the last year's position
        middle_index = index - 6
        year_positions.append(middle_index)
        year_labels.append(current_year)

        # Configure the X-axis
        xticks = range(len(months))
        ax.set_xticks(xticks)
        ax.set_xticklabels(month_labels, rotation=0)

        # Add year labels at the middle of each year's range
        for pos, year in zip(year_positions, year_labels):
            ax.text(
                pos, -0.5, str(year), fontsize=10, ha="center", transform=ax.get_xaxis_transform()
            )

        ax.tick_params(axis='x', which='both', bottom=False, top=False)  # Disable default ticks

    def show_entries_scene(self, event=None):
        self.hide()
        self.app.show_entries_scene()

    def clear_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # After clearing widgets, reset the scroll region to avoid an empty space scroll
        self.canvas.config(scrollregion=self.canvas.bbox("all"))