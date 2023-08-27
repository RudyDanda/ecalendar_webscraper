# ecalendar_webscraper

This repository contains a web scraper designed to extract economic calendar data from [TradingEconomics.com](https://www.tradingeconomics.com/).

## Features

- Extracts comprehensive economic event data, including event name, country, date, and more.
- Utilizes [Playwright](https://playwright.dev/) for web navigation and scraping.
- Processes and structures data using the [Pandas](https://pandas.pydata.org/) library in Python.

## Prerequisites

Ensure the following requirements have been met:

- [Python 3.x](https://www.python.org/downloads/)
- Playwright: Install via pip with `pip install playwright`
- Pandas: Install via pip with `pip install pandas`

## How to Use

1. **Clone the Repository**:
git clone https://github.com/RudyDanda/ecalendar_webscraper.git
cd ecalendar_webscraper
2. **Modify the arguments in the main file**: Enter the year range you want to receive data in the main file
3. **Run the Scraper**: python main.py
4. **Output**:
The data will be saved in a XLSX file named `economic_data.xlsx` in the current directory.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Thanks to [TradingEconomics.com](https://www.tradingeconomics.com/) for providing the data.
