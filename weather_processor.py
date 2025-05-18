"""
Name: Raghav Sharma
Date: 2025-04-15
Description: This module processes raw weather data into a structured format.
"""

import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="weather_processor.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class WeatherProcessor:
    """
    A class to process raw weather data into a structured format.
    """

    def __init__(self, raw_data):
        """
        Initialize the processor with raw scraped data.
        :param raw_data: List of dictionaries containing daily weather information.
        """
        self.raw_data = raw_data

    def transform_data(self):
        """
        Convert raw list of weather data into a dictionary format:
        {
            "YYYY-MM-DD": {"Min": float or None, "Max": float or None, "Mean": float or None},
            ...
        }
        :return: Dictionary of cleaned weather data.
        """
        processed_data = {}

        for entry in self.raw_data:
            try:
                # Validate and parse date
                date_str = entry["date"]
                datetime.strptime(date_str, "%Y-%m-%d")

                # Safely parse temperature values
                min_temp = entry.get("min_temp", None)
                max_temp = entry.get("max_temp", None)
                mean_temp = entry.get("mean_temp", None)

                processed_data[date_str] = {
                    "Min": float(min_temp) if min_temp is not None else None,
                    "Max": float(max_temp) if max_temp is not None else None,
                    "Mean": float(mean_temp) if mean_temp is not None else None,
                }

            except (ValueError, TypeError) as e:
                logging.error("Skipping invalid entry %s: %s", entry, e)
                print(f"Skipping invalid entry {entry}: {e}")
                continue

        return processed_data