import csv

# Define the input and output CSV file names
input_csv_file = 'archive_urls.csv' 
output_csv_file = 'output.csv' 

# Create an empty list to store unique rows and a set to track seen dates
unique_rows = []
seen_dates = set()

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

        # If this date hasn't been seen yet, add the row to the list
        if date_part not in seen_dates:
            seen_dates.add(date_part)
            unique_rows.append(row)

# Write the filtered unique rows to the output CSV
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(unique_rows)

print(f"Filtered CSV has been saved to {output_csv_file}")

# Script by Bishal TImsina
