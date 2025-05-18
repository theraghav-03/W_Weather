"""
Name: Raghav Sharma
Date: 2025-04-15
Description: This module handles all plotting operations for the weather data.
"""

import logging
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Configure logging
logging.basicConfig(
    filename="plot_operations.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class PlotOperations:
    """
    A class to handle plotting operations for weather data.
    """

    def __init__(self, data):
        """
        Initialize with weather data (list of tuples).
        Each tuple: (id, sample_date, location, min_temp, max_temp, avg_temp).
        :param data: List of tuples containing weather data.
        """
        self.data = data

    def generate_year_to_year_boxplot(self, start_year, end_year):
        """
        Generate a boxplot of mean temperatures for a given date range (year to year).
        Displays one box per month (January to December).
        :param start_year: Start year for the range.
        :param end_year: End year for the range.
        """
        try:
            month_data = defaultdict(list)

            for record in self.data:
                date_str, mean_temp = record[1], record[5]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if start_year <= date_obj.year <= end_year and mean_temp is not None:
                    month_data[date_obj.month].append(mean_temp)

            if not month_data:
                print(f"No data available for the range {start_year}-{end_year}")
                return

            # Prepare data for plotting
            labels = [datetime(1900, month, 1).strftime('%B') for month in range(1, 13)]
            values = [month_data[month] for month in range(1, 13) if month in month_data]

            plt.boxplot(values, labels=labels)
            plt.title(f"Year-to-Year Mean Temperature Distribution ({start_year}-{end_year})")
            plt.xlabel("Month")
            plt.ylabel("Mean Temperature (°C)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            logging.error("Error in generate_year_to_year_boxplot: %s", e)
            print(f"An error occurred: {e}")

    def generate_lineplot(self, year, month):
        """
        Generate a line plot of daily mean temperatures for a given month/year.
        :param year: Year for the plot.
        :param month: Month for the plot.
        """
        try:
            days = []
            temps = []

            for record in self.data:
                date_str, mean_temp = record[1], record[5]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj.year == year and date_obj.month == month and mean_temp is not None:
                    days.append(date_obj.day)
                    temps.append(mean_temp)

            if not days:
                print(f"No data available for {year}-{month:02d}")
                return

            plt.plot(days, temps, marker='o', linestyle='-', color='tab:blue')
            plt.title(f"Daily Mean Temperatures for {year}-{month:02d}")
            plt.xlabel("Day of the Month")
            plt.ylabel("Mean Temperature (°C)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            logging.error("Error in generate_lineplot: %s", e)
            print(f"An error occurred: {e}")