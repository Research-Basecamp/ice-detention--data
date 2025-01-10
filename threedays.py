import csv
from datetime import datetime

# Define the input and output CSV file names
input_csv_file = 'threedaystime.csv'  # Replace with your input CSV file path
output_csv_file = 'onedaystime.csv'  # Replace with the desired output CSV file path

# Create an empty list to store the unique rows
unique_rows = []
seen_dates = set()  # To store dates we've already encountered
last_date = None  # To track the last added date

# Open the input CSV file and read it
with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)  # Extract header row
    
    # Append header to the unique_rows
    unique_rows.append(header)

    # Iterate over the rows in the CSV
    for row in reader:
        archive_url = row[0]  # Assuming the URL is in the first column (index 0)

        # Extract the date portion from the timestamp (first 8 characters)
        date_part = archive_url.split('/')[4][:8]  # Extract the first 8 digits from the timestamp
        
        # Convert the date part to a datetime object for comparison
        current_date = datetime.strptime(date_part, '%Y%m%d')

        # If we haven't seen this date yet and it's at least 3 days apart from the last date
        if date_part not in seen_dates and (last_date is None or (current_date - last_date).days >= 4):
            seen_dates.add(date_part)
            unique_rows.append(row)
            last_date = current_date  # Update the last date to the current one

# Write the filtered rows into the output CSV file
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(unique_rows)

print(f"Filtered CSV has been saved to {output_csv_file}")
