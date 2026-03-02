import pandas as pd
import argparse
import logging
import sys
import os

# Set up simple logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def convert_csv_to_excel(input_file, output_file):
    """Reads a CSV, cleans the data, and exports it to an Excel file."""
    
    # Check if input file exists before trying to read it
    if not os.path.exists(input_file):
        logging.error(f"File not found: {input_file}. Please check the path and try again.")
        sys.exit(1)

    try:
        logging.info(f"Reading CSV file: {input_file}")
        # 1. Read CSV files
        df = pd.read_csv(input_file)
        
        # Check if the dataframe is empty
        if df.empty:
            logging.warning("The input CSV file is empty. Proceeding anyway, but output will be empty.")

        logging.info("Cleaning and normalizing data...")

        # 2. Handle missing values
        # Example: Fill missing numeric values with 0 and strings with 'Unknown'
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna("Unknown")

        # 3. Date parsing
        # Example: Automatically look for columns with 'date' in the name and parse them
        for col in df.columns:
            if 'date' in col.lower():
                logging.info(f"Parsing dates in column: '{col}'")
                # errors='coerce' turns invalid dates into NaT (Not a Time)
                df[col] = pd.to_datetime(df[col], errors='coerce') 

        # 4. Simple column renames
        # Example: Standardize column names (lowercase, replace spaces with underscores)
        logging.info("Standardizing column names...")
        df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

        # 5. Export to .xlsx
        logging.info(f"Exporting data to Excel: {output_file}")
        # index=False prevents pandas from writing row numbers into the Excel file
        df.to_excel(output_file, index=False, engine='openpyxl')
        
        logging.info("Conversion completed successfully! 🎉")

    except pd.errors.EmptyDataError:
        logging.error("The provided CSV file contains no data or columns.")
        sys.exit(1)
    except pd.errors.ParserError:
        logging.error("Error parsing the CSV file. It might be corrupted or incorrectly formatted.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Setup CLI flags using argparse
    parser = argparse.ArgumentParser(
        description="A script to convert CSV files to Excel with basic data cleaning."
    )
    
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Path to the input CSV file"
    )
    parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="Path to save the output Excel file (.xlsx)"
    )

    args = parser.parse_args()

    # Ensure output file ends with .xlsx
    if not args.output.lower().endswith('.xlsx'):
        logging.warning("Output file doesn't end with .xlsx. Appending it automatically.")
        args.output += '.xlsx'

    # Execute the conversion
    convert_csv_to_excel(args.input, args.output)