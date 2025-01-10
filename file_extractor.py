import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import re
from time import sleep
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd

# Constants
TIMEOUT = 10
MAX_RETRIES = 3
DOWNLOAD_DIR = 'downloaded_files'

# Retry and timeout handling
def get_with_retry(url, **kwargs):
    session = requests.Session()
    retries = Retry(total=MAX_RETRIES, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, timeout=TIMEOUT, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to process the page and download .xlsx files
def process_page(url):
    response = get_with_retry(url)

    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        xlsx_links = [urljoin(url, link['href']) for link in links if link['href'].endswith('.xlsx')]

        if xlsx_links:
            if not os.path.exists(DOWNLOAD_DIR):
                os.makedirs(DOWNLOAD_DIR)

            for xlsx_url in xlsx_links:
                print(f"Processing {xlsx_url}...")

                match = re.search(r'web/(\d{14})/', xlsx_url)
                timestamp = match.group(1) if match else "unknown_timestamp"
                year_int = int(timestamp[:4])
                fiscal_year_prefix = f"FY{year_int - 2000:02d}"
                file_name = xlsx_url.split('/')[-1]

                if fiscal_year_prefix in file_name:
                    new_file_name = f"{timestamp}-{file_name}"
                    file_path = os.path.join(DOWNLOAD_DIR, new_file_name)

                    file_response = get_with_retry(xlsx_url)
                    if file_response:
                        with open(file_path, 'wb') as file:
                            file.write(file_response.content)
                        print(f"Downloaded {file_path}")
                    else:
                        print(f"Failed to download {xlsx_url}.")
                else:
                    print(f"Skipping {file_name} as it doesn't match fiscal year prefix {fiscal_year_prefix}.")
        else:
            print("No Excel files found on the page.")
    else:
        print(f"Failed to fetch the webpage {url}.")

# Load CSV and filter unique rows by 'Update Time'
csv_file_path = 'cleaned_data.csv'  # Replace with your file path
df = pd.read_csv(csv_file_path)
df_unique = df[df['Update Time'] != df['Update Time'].shift()]

# Iterate over each unique Archive URL
for index, row in df_unique.iterrows():
    archive_url = row['Archive URL']
    print(f"Processing URL: {archive_url}")
    process_page(archive_url)
    sleep(1)  # Pause to avoid server overload
