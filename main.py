"""
Name: Raghav Sharma
Date: 2025-04-15
Description: This module serves as the main entry point for the Weather Processing App.
"""

import logging
from scrape_weather import fetch_weather_data
from plot_operations import PlotOperations
from weather_processor import WeatherProcessor
from db_operations import DBOperations
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="main.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_all_data():
    """
    Scrape all available weather data from 2020 to the current date
    and save it to the database.
    """
    try:
        db = DBOperations()
        existing_records = db.fetch_data()
        existing_dates = {record[1] for record in existing_records}

        print("Scraping all weather data from 2020 to the current date...")
        raw_data = fetch_weather_data()
        if not raw_data:
            print("No data fetched.")
            db.close_connection()
            return

        new_data = [record for record in raw_data if record["date"] not in existing_dates]

        if new_data:
            processor = WeatherProcessor(new_data)
            processed_data = processor.transform_data()
            db.save_data(processed_data)
            print("New data has been saved to the database.")
        else:
            print("No new data to save.")

        db.close_connection()
        print("Completed scraping all available data.")
    except Exception as e:
        logging.error("Error in scrape_all_data: %s", e)
        print(f"An error occurred: {e}")

def view_boxplot():
    """
    Generate a year-to-year boxplot for weather data within a specified range.
    """
    try:
        start_year = int(input("Enter start year (e.g., 2023): "))
        end_year = int(input("Enter end year (e.g., 2024): "))

        db = DBOperations()
        data = db.fetch_data()
        db.close_connection()

        if not data:
            print("No data available for plotting.")
            return

        plotter = PlotOperations(data)
        plotter.generate_year_to_year_boxplot(start_year, end_year)
    except ValueError as e:
        logging.error("Invalid input for year range: %s", e)
        print(f"Invalid input: {e}")
    except Exception as e:
        logging.error("Error in view_boxplot: %s", e)
        print(f"An error occurred: {e}")

def view_lineplot():
    """
    Generate a line plot for weather data for a specific year and month.
    """
    try:
        year = int(input("Enter year (e.g., 2023): "))
        month = int(input("Enter month (1-12): "))

        db = DBOperations()
        data = db.fetch_data()
        db.close_connection()

        plotter = PlotOperations(data)
        plotter.generate_lineplot(year, month)
    except ValueError as e:
        logging.error("Invalid input for year or month: %s", e)
        print(f"Invalid input: {e}")
    except Exception as e:
        logging.error("Error in view_lineplot: %s", e)
        print(f"An error occurred: {e}")

def main():
    """
    Main function to display the menu and handle user input.
    """
    while True:
        try:
            print("\nWelcome to the WeatherScrapy!")
            print("1. Scrape All Available Weather Data")
            print("2. View Weather Trends (Boxplot)")
            print("3. View Monthly Weather (Line Plot)")
            print("4. Exit")

            choice = input("Please enter a number from 1 - 4: ").strip()

            if choice == '1':
                scrape_all_data()
            elif choice == '2':
                view_boxplot()
            elif choice == '3':
                view_lineplot()
            elif choice == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid input. Please enter a number between 1 and 4.")
        except Exception as e:
            logging.error("Error in main menu: %s", e)
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()