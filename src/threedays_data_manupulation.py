import csv
from datetime import datetime

# Define the input and output CSV file names
input_csv_file = 'threedaystime.csv'  
output_csv_file = 'onedaystime.csv' 

# Create an empty list to store unique rows and a set to track seen dates
unique_rows = []
seen_dates = set()
last_date = None  # To track the last added date

# Open and read the input CSV file
with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)  # Extract the header row
    unique_rows.append(header)  # Append header to the unique rows list

    # Iterate over each row in the input CSV
    for row in reader:
        archive_url = row[0]  # Archive URL is in the first column

        # Extract the date portion from the timestamp (first 8 characters)
        date_part = archive_url.split('/')[4][:8]  # e.g., '20230517'

        # Convert the date part to a datetime object for comparison
        current_date = datetime.strptime(date_part, '%Y%m%d')

        # If the date hasn't been seen and it's at least 4 days apart from the last date
        if date_part not in seen_dates and (last_date is None or (current_date - last_date).days >= 4):
            seen_dates.add(date_part)
            unique_rows.append(row)
            last_date = current_date  # Update the last date to the current one

# Write the filtered unique rows to the output CSV
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(unique_rows)

print(f"Filtered CSV has been saved to {output_csv_file}")

# Script by Bishal Timsina
