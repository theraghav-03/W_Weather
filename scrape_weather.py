"""
Name: Raghav Sharma
Date: 2025-04-15
Description: This module handles all web scraping operations for weather data.
"""

import logging
import requests
from html.parser import HTMLParser
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="scrape_weather.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class WeatherScraper(HTMLParser):
    """
    A class to parse weather data from HTML content.
    """

    def __init__(self, year, month):
        """
        Initialize the WeatherScraper with the year and month to scrape.
        :param year: Year of the data to scrape.
        :param month: Month of the data to scrape.
        """
        super().__init__()
        self.year = year
        self.month = month
        self.in_table = False
        self.in_row = False
        self.current_data = []
        self.weather_data = []
        self.capture_data = False
        self.current_tag = ""

    def handle_starttag(self, tag, attrs):
        """
        Handle the start of an HTML tag.
        """
        try:
            if tag == "table":
                self.in_table = True
            elif self.in_table and tag == "tr":
                self.in_row = True
                self.current_data = []
            elif self.in_table and tag in ["th", "td"]:
                self.capture_data = True
            self.current_tag = tag
        except Exception as e:
            logging.error("Error in handle_starttag: %s", e)

    def handle_data(self, data):
        """
        Handle the data within an HTML tag.
        """
        try:
            if self.capture_data:
                cleaned_data = data.strip()
                if cleaned_data and cleaned_data not in ["LegendM", "M", "LegendE", "E"]:
                    self.current_data.append(cleaned_data)
        except Exception as e:
            logging.error("Error in handle_data: %s", e)

    def handle_endtag(self, tag):
        """
        Handle the end of an HTML tag.
        """
        try:
            if tag in ["th", "td"]:
                self.capture_data = False
            elif tag == "tr" and self.in_row:
                self.in_row = False
                if len(self.current_data) >= 5:
                    try:
                        day = self.current_data[0].zfill(2)
                        full_date = f"{self.year}-{self.month:02d}-{day}"

                        self.weather_data.append({
                            "date": full_date,
                            "max_temp": float(self.current_data[1]) if self.current_data[1] != "-" else None,
                            "min_temp": float(self.current_data[2]) if self.current_data[2] != "-" else None,
                            "mean_temp": float(self.current_data[3]) if self.current_data[3] != "-" else None,
                        })
                    except ValueError as e:
                        logging.error("Error parsing row data: %s", e)
            elif tag == "table":
                self.in_table = False
        except Exception as e:
            logging.error("Error in handle_endtag: %s", e)

    def get_weather_data(self):
        """
        Retrieve the parsed weather data.
        :return: List of dictionaries containing weather data.
        """
        return self.weather_data


def fetch_weather_data():
    """
    Fetch weather data from 2020 to the current date.
    :return: List of weather data dictionaries.
    """
    try:
        start_year = 2020
        current_year = datetime.now().year
        current_month = datetime.now().month
        all_weather_data = []

        for year in range(start_year, current_year + 1):
            for month in range(1, 13):
                if year == current_year and month > current_month:
                    break  # Stop if the month is beyond the current month in the current year

                print(f"Fetching data for {year}-{month:02d}...")
                base_url = "https://climate.weather.gc.ca/climate_data/daily_data_e.html"
                params = {
                    "StationID": 27174,  # Winnipeg Station ID
                    "timeframe": 2,      # Daily data
                    "StartYear": year,
                    "Year": year,
                    "Month": month
                }

                query_string = "&".join(f"{key}={value}" for key, value in params.items())
                full_url = f"{base_url}?{query_string}"

                try:
                    response = requests.get(full_url)
                    if response.status_code == 200:
                        parser = WeatherScraper(year, month)
                        parser.feed(response.text)
                        monthly_data = parser.get_weather_data()
                        if monthly_data:
                            all_weather_data.extend(monthly_data)
                    else:
                        logging.error("Failed to fetch data for %s-%02d: %s", year, month, response.status_code)
                        print(f"Failed to fetch data for {year}-{month:02d}: {response.status_code}")
                except requests.RequestException as e:
                    logging.error("Error fetching data for %s-%02d: %s", year, month, e)
                    print(f"Error fetching data for {year}-{month:02d}: {e}")

        return all_weather_data
    except Exception as e:
        logging.error("Error in fetch_weather_data: %s", e)
        print(f"An error occurred: {e}")
        return []