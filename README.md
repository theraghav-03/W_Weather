### We_Weather
Weather Data Processing App
A Python application that scrapes historical weather data for Winnipeg from Environment Canada, stores it in a SQLite database, and visualizes trends through an interactive GUI.

🔧 Features

✅ Scrapes min, max, and mean temperatures using a custom HTML parser

✅ Stores data in a structured SQLite database with validation to prevent duplicates

✅ Interactive Tkinter GUI for user input and navigation

✅ Visualizes data with Matplotlib using:

📊 Boxplots for monthly trends across years

📈 Line charts for daily temperatures in a specific month/year

✅ Modular architecture with separate components for scraping, database handling, and plotting

📂 Technologies Used
Python 3

HTMLParser

SQLite

Tkinter

Matplotlib

Logging (for error tracking)

🚀 Getting Started
Clone the repository

Run weather_processor.py to launch the application

Use the GUI to scrape, update, and visualize weather data

📌 Notes
No hardcoded end dates – the scraper automatically detects the last available data

All components follow PEP8 standards and are documented for maintainability
