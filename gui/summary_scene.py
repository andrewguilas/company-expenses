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
                for month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                    date_string = f"{year}_{month}"

                    # Initialize the dictionary for the location, category, and month
                    if date_string not in stats[entry.location][entry.category]:
                        stats[entry.location][entry.category][date_string] = {
                            "YEAR": year,
                            "MONTH": month,
                            "COUNT": 0,
                            "AMOUNT": 0
                        }

            date_string = f"{entry.date.year}_{entry.date.month}"
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

        # Calculate the maximum amount across all categories for consistent Y-axis scaling
        global_max = 0
        for location, categories in stats.items():
            for category, data in categories.items():
                if category == selected_category:
                    global_max = max(global_max, max(data[month]["AMOUNT"] for month in data))

        # Collect all locations to determine the number of histograms
        locations = [location for location in stats]
        num_locations = len(locations)

        # Dynamic figure height adjustment
        total_canvas_height = 800  # Total height available for all histograms
        histogram_height = total_canvas_height / num_locations  # Height for each histogram

        # Create a single figure with multiple subplots
        fig, axes = plt.subplots(
            num_locations, 1, figsize=(10, total_canvas_height / 100),
            sharex=True, sharey=True, constrained_layout=True
        )
        if num_locations == 1:
            axes = [axes]  # Ensure axes is always a list for uniform handling

        for ax, location in zip(axes, locations):
            for category, data in stats[location].items():
                if category == selected_category:
                    self.display_histogram(ax, category, data, global_max)

            ax.set_title(location, fontsize=10)
            ax.set_ylim(0, global_max)

        # Add the figure to the canvas
        fig.patch.set_facecolor('white')
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def display_histogram(self, ax, category, data, global_max):
        MIN_DATE = "2022_1"
        MAX_DATE = "2023_12"

        # Prepare data for histogram (month_year vs amount)
        month_years = sorted(data.keys())
        amounts = [data[my]["AMOUNT"] for my in month_years]

        # Define the range of months to include all months even with no data
        start_date = datetime.strptime(MIN_DATE, "%Y_%m")
        end_date = datetime.strptime(MAX_DATE, "%Y_%m")

        months = []
        current_date = start_date
        while current_date <= end_date:
            months.append(current_date.strftime("%Y_%m"))
            current_date += relativedelta(months=1)

        # Initialize the full data dictionary with zero amounts for missing months
        full_data = {month: 0 for month in months}
        for month_year in month_years:
            full_data[month_year] = data[month_year]["AMOUNT"]

        amounts = [full_data[month] for month in months]

        # Plot the histogram
        ax.bar(months, amounts, label=category)
        ax.tick_params(axis="x", rotation=90)
        ax.legend(fontsize=8)

    def show_entries_scene(self, event=None):
        self.hide()
        self.app.show_entries_scene()

    def clear_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # After clearing widgets, reset the scroll region to avoid an empty space scroll
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
