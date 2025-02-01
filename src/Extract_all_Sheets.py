import os
import requests
from waybackpy import WaybackMachine
from bs4 import BeautifulSoup

# Configure target URL
target_url = "https://www.ice.gov/doclib/detention/"

# Set up WaybackMachine object with the target URL
wayback = WaybackMachine(target_url)

# Fetch the most recent snapshot available for the target URL
wayback.get()
print(f"Using snapshot URL: {wayback.url}")

# Directory to store the downloaded files
download_dir = 'downloaded_files'
os.makedirs(download_dir, exist_ok=True)

# Send a request to the Wayback Machine's snapshot
response = requests.get(wayback.url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract all file links from the page (filtering by file extensions)
links = soup.find_all('a', href=True)
for link in links:
    file_url = link['href']
    if file_url.endswith(('.xlsx', '.csv', '.pdf')):  # Filter by file type
        file_name = file_url.split("/")[-1]
        file_path = os.path.join(download_dir, file_name)
        
        # Check if the URL is a relative link (i.e., missing domain)
        if file_url.startswith('/'):
            file_url = 'https://web.archive.org' + file_url
        
        # Download the file
        file_response = requests.get(file_url)
        with open(file_path, 'wb') as f:
            f.write(file_response.content)
        print(f"Downloaded: {file_name}")

print("Download process completed.")
