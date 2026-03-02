# CSV to Excel Converter 📊

A Python command-line utility that automates the process of cleaning, normalizing, and converting raw CSV data into formatted Excel (`.xlsx`) reports. 

## Features
* **Automated Data Cleaning:** Handles missing numeric and text values.
* **Smart Date Parsing:** Automatically detects date columns and formats them properly.
* **Header Standardization:** Converts column headers to clean, lowercase snake_case format.
* **Command Line Interface:** Easy to run via terminal with input/output flags.
* **Error Handling:** Built-in logging to track progress and catch bad data.

## Prerequisites
You will need Python installed along with `pandas` and `openpyxl`. 

```bash
pip install pandas openpyxl
