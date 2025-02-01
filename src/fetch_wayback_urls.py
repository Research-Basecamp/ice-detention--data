import os
from waybackpy import WaybackMachineCDXServerAPI
import csv

# Define the target URL and user agent
target_url = "https://www.ice.gov/detain/detention-management"
user_agent_string = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"

# Initialize the Wayback Machine CDX Server API with a specific time range
wayback_api = WaybackMachineCDXServerAPI(
    target_url, 
    user_agent_string, 
    start_timestamp=2021, 
    end_timestamp=2025
)

# File names
text_file_name = "archive_urls.txt"
csv_file_name = "archive_urls.csv"

# Ensure the text file exists
if not os.path.exists(text_file_name):
    with open(text_file_name, 'w') as f:
        pass

# Ensure the CSV file exists with the header
if not os.path.exists(csv_file_name):
    with open(csv_file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Archive URL"])  # Adding header

# Save archive URLs to the files
with open(text_file_name, 'a') as txt_file, open(csv_file_name, 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    for snapshot in wayback_api.snapshots():
        archive_url = snapshot.archive_url
        txt_file.write(f"{archive_url}\n")
        csv_writer.writerow([archive_url])
