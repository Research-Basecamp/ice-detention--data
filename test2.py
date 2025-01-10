import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv  # Import the correct csv module

# File path for the CSV containing the URLs
csv_path = 'output.csv'

# Function to extract update time
def extract_update_time(url):
    try:
        print(f"Processing URL: {url}")  # Log the URL being processed
        # Send a GET request to the archived URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful (200 OK)
        
        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for the span with the update time
        update_time_element = soup.find('span', class_='field-content')
        if update_time_element:
            update_time = update_time_element.get_text(strip=True)
            print(f"Extracted Update Time: {update_time}")  # Log the extracted update time
            return update_time
        else:
            print("Update time not found in the page.")  # Log if no update time found
            return "Update time not found"
    except requests.RequestException as e:
        # Handle any exceptions (e.g., network errors)
        print(f"Error fetching {url}: {e}")  # Log the error
        return "Error fetching URL"

# Read the CSV file containing the URLs
df = pd.read_csv(csv_path)

# Check if 'Archive URL' column exists
if 'Archive URL' not in df.columns:
    raise ValueError("The CSV file must contain a column named 'Archive URL'")

# Create a new file or open an existing file to write the results in real-time
new_csv_path = 'new1.csv'

# Open the file and write the header only once
with open(new_csv_path, 'w', newline='', encoding='utf-8') as file:
    # Define the CSV writer
    writer = csv.writer(file)
    writer.writerow(['Archive URL', 'Update Time'])  # Write the header

    # Process each URL and save the result immediately
    for url in df['Archive URL']:
        update_time = extract_update_time(url)

        # Write the URL and its corresponding update time to the CSV file in real-time
        writer.writerow([url, update_time])

        print(f"URL: {url} processed and saved.")

print(f"New CSV file with update times saved at: {new_csv_path}")
