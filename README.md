# ICE Detention Data Processing

This project processes and manipulates data related to ICE detention statistics, specifically for fiscal years 2021-2025. The data is extracted from Excel files available from the Wayback Machine, cleaned, and transformed into a structured format for analysis.

## Project Structure


ice-detention--data/
├── All_Excel_sheets
├── README.md
├── assests
├── requirment.txt
└── src
    ├── Extract_all_Sheets.py
    ├── data_processing.py
    ├── download_xlsx_from_wayback.py
    ├── extract_update_times.py
    ├── fetch_wayback_urls.py
    ├── filter_unique_dates.py
    └── threedays_data_manupulation.py


## Overview

The project consists of several Python scripts aimed at downloading, processing, and transforming historical detention data into a structured and clean format. The primary goal is to clean and filter the data to generate a consolidated dataset that can be easily analyzed.

### Key Features:

1.  **Data Downloading**:

    -   `download_xlsx_from_wayback.py` is responsible for downloading Excel files from the Wayback Machine based on a list of URLs.
    -   The files are then saved in a designated directory (`All_Excel_sheets`).
2.  **Data Extraction**:

    -   `Extract_all_Sheets.py` extracts relevant sheets from the downloaded Excel files.
    -   `data_processing.py` reads the relevant sheets, extracts the necessary data (such as ICE and CBP detention statistics), and compiles it into a structured format.
3.  **Data Cleaning**:

    -   The script ensures that only unique rows are kept based on specific criteria, such as dates and update times. This is handled by `filter_unique_dates.py` and `threedays_data_manupulation.py`.
4.  **Consolidation**:

    -   After extraction and filtering, the data is saved into two formats: `Data_processing.csv` and `Data_processing.xlsx`, for further analysis or use in downstream applications.

## Setup Instructions

1.  **Clone the Repository**:



    `git clone https://github.com/Research-Basecamp/TRAC-Imigration-Report`

2.  **Install Dependencies**: Ensure you have Python installed and then install the required dependencies using `pip`:


    `pip install -r requirements.txt`

3.  **Download Data**: To download the Excel files, run the `download_xlsx_from_wayback.py` script. This will use the URLs from the provided CSV file (`all_snapshot_urls.csv`) to fetch the necessary historical data from the Wayback Machine.


    `python src/download_xlsx_from_wayback.py`
    

4.  **Process Data**: After downloading the data, use the `data_processing.py` script to clean and combine the data into a single dataset.

    bash
    Copy

    `python src/data_processing.py`

5.  **Filter Unique Dates**: The `filter_unique_dates.py` script removes duplicate data based on unique date entries.

    bash
    Copy

    `python src/filter_unique_dates.py`

6.  **Manipulate Dates**: The `threedays_data_manupulation.py` script ensures that the filtered data follows a minimum 3-day interval rule for better consistency.


    `python src/threedays_data_manupulation.py`


## Output

After running the processing scripts, the output will be saved in two formats:

-   `Data_processing.xlsx` - Excel format of the cleaned and processed data.
-   `Data_processing.csv` - CSV format of the cleaned and processed data.

## Dependencies

-   `pandas` - Data manipulation and analysis.
-   `requests` - HTTP library for fetching data from URLs.
-   `beautifulsoup4` - HTML parsing for scraping data from the Wayback Machine.
-   `openpyxl` - Reading and writing Excel files.
-   `re` - Regular expressions for parsing and matching patterns.
-   `csv` - Handling CSV files.
-   `datetime` - Handling date and time operations.

### Install dependencies with:

`pip install -r requirements.txt`

## Notes

-   This project assumes that the data sheets in the Excel files follow a specific structure. Any deviations in the file format or structure might require adjustments in the processing scripts.
-   The Wayback Machine URLs provided in `all_snapshot_urls.csv` must be correct and accessible for the downloading process to work.