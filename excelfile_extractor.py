import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
url = "https://web.archive.org/web/20240101120358/https://www.ice.gov/detain/detention-management"

# Send a GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Raise an error if the request fails

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the <a> tag with the class 'survey-processed'
excel_link_tag = soup.find('a', class_='survey-processed')

if excel_link_tag:
    # Extract the href attribute (URL of the Excel file)
    excel_file_url = excel_link_tag['href']
    print(f"Found the Excel file URL: {excel_file_url}")
else:
    print("The link with class 'survey-processed' was not found.")