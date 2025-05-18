"""
Name: Raghav Sharma
Date: 2025-04-15
Description: This module handles all database operations including
initializing the database, saving weather data, fetching data, and purging data.
"""

import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="db_operations.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DBOperations:
    """
    A class to handle database operations for weather data.
    This includes initializing the database, saving data, fetching data,
    and purging data.
    """

    def __init__(self, db_name="weather_data.db"):
        """
        Initialize the database connection and create the table if it doesn't exist.
        :param db_name: Name of the SQLite database file.
        """
        self.db_name = db_name
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.initialize_db()
        except sqlite3.Error as e:
            logging.error("Error initializing database connection: %s", e)

    def initialize_db(self):
        """
        Create the weather_data table if it doesn't exist.
        """
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_date TEXT NOT NULL,
                location TEXT NOT NULL DEFAULT 'Winnipeg',
                min_temp REAL,
                max_temp REAL,
                avg_temp REAL,
                UNIQUE(sample_date, location)  -- Ensures each date-location pair is unique
            );
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error("Error creating table: %s", e)

    def save_data(self, weather_dict):
        """
        Save weather data to the database while ensuring the date is in 'YYYY-MM-DD' format.
        :param weather_dict: Dictionary containing weather data.
        """
        insert_query = """
        INSERT OR IGNORE INTO weather_data (sample_date, location, min_temp, max_temp, avg_temp)
        VALUES (?, ?, ?, ?, ?);
        """
        for date_str, temps in weather_dict.items():
            try:
                # Ensure the date is stored in 'YYYY-MM-DD' format
                formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
                self.cursor.execute(insert_query, (
                    formatted_date, "Winnipeg", temps["Min"], temps["Max"], temps["Mean"]
                ))
            except ValueError as e:
                logging.error("Invalid date format for '%s': %s", date_str, e)
            except sqlite3.Error as e:
                logging.error("Error inserting data into database: %s", e)
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error("Error committing transaction: %s", e)

    def fetch_data(self, start_date=None, end_date=None):
        """
        Retrieve weather data from the database within a given range.
        :param start_date: Start date in 'YYYY-MM-DD' format (optional).
        :param end_date: End date in 'YYYY-MM-DD' format (optional).
        :return: List of tuples containing weather data.
        """
        query = "SELECT id, sample_date, location, min_temp, max_temp, avg_temp FROM weather_data"
        params = []
        if start_date and end_date:
            query += " WHERE sample_date BETWEEN ? AND ?"
            params = [start_date, end_date]
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error("Error fetching data from database: %s", e)
            return []

    def purge_data(self):
        """
        Delete all records while keeping the database structure intact.
        """
        try:
            self.cursor.execute("DELETE FROM weather_data;")
            self.conn.commit()
            print("All weather data has been deleted.")
        except sqlite3.Error as e:
            logging.error("Error purging data from database: %s", e)

    def close_connection(self):
        """
        Close the database connection.
        """
        try:
            self.conn.close()
        except sqlite3.Error as e:
            logging.error("Error closing database connection: %s", e)