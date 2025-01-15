import pandas as pd
import re
import os

# Directory containing the files
folder_path = "downloaded_files"

# List all the Excel files in the directory
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Initialize an empty list to store the results
combined_results = []

# List of possible sheet names
possible_sheet_names = [
    "Detention FY21 YTD", "Detention FY22", "Detention FY23", "Detention FY24", "Detention FY25"
]

# Loop through each file in the folder
for file_path in file_paths:
    print(f"Processing file: {file_path}")
    
    # Try to read the relevant sheet from the file
    sheet_data = None
    for sheet_name in possible_sheet_names:
        try:
            # Try to read the sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            sheet_data = sheet_name
            print(f"Found sheet: {sheet_name}")
            break  # Stop once the sheet is found
        except ValueError:
            # Skip if the sheet does not exist in the file
            continue
    
    # If a relevant sheet is found, process the data
    if sheet_data:
        # Identify the rows dynamically based on known keywords
        start_row = 18  # Adjust based on actual data structure
        end_row = 22  # Includes "Other Immigration Violator"
        data_columns = [0, 1, 3]  # Extract only relevant columns (Criminality, ICE, CBP)

        # Extract the relevant rows and columns
        table_data = df.iloc[start_row:end_row + 1, data_columns]

        # Rename the columns for clarity
        table_data.columns = ["Criminality", "ICE", "CBP"]

        # Transform the table to the required format
        extracted_data = {
            "File Name": os.path.basename(file_path),  # Add file name to the extracted data
            "ICE_Convicted Criminal": table_data.loc[table_data["Criminality"] == "Convicted Criminal", "ICE"].values[0],
            "CBP_Convicted Criminal": table_data.loc[table_data["Criminality"] == "Convicted Criminal", "CBP"].values[0],
            "ICE_Pending Charges": table_data.loc[table_data["Criminality"] == "Pending Criminal Charges", "ICE"].values[0],
            "CBP_Pending Charges": table_data.loc[table_data["Criminality"] == "Pending Criminal Charges", "CBP"].values[0],
            "ICE_other Violator": table_data.loc[table_data["Criminality"] == "Other Immigration Violator", "ICE"].values[0],
            "CBP_other Violator": table_data.loc[table_data["Criminality"] == "Other Immigration Violator", "CBP"].values[0],
        }

        # Read the 'Footnotes' sheet to extract term and definition information
        footnotes_df = pd.read_excel(file_path, sheet_name="Footnotes", header=None)

        # Extract the term and definition from rows 50 and 51 (index 49 and 50 in 0-based indexing)
        term_info_50 = footnotes_df.iloc[49, 0]  # Assuming term is in column 0 of row 50
        definition_info_50 = footnotes_df.iloc[49, 1]  # Assuming definition is in column 1 of row 50
        term_info_51 = footnotes_df.iloc[50, 0]  # Assuming term is in column 0 of row 51
        definition_info_51 = footnotes_df.iloc[50, 1]  # Assuming definition is in column 1 of row 51

        # Try to extract the EID date from both rows 50 and 51
        eid_date_match_50 = re.search(r"EID as of (\d{2}/\d{2}/\d{4})", definition_info_50)
        eid_date_match_51 = re.search(r"EID as of (\d{2}/\d{2}/\d{4})", definition_info_51)

        # If an EID date is found in row 50, use it, otherwise check row 51
        if eid_date_match_50:
            eid_date = eid_date_match_50.group(1)
        elif eid_date_match_51:
            eid_date = eid_date_match_51.group(1)
        else:
            eid_date = None  # Handle case if no match is found in either row

        # Add the EID Date to the extracted data
        extracted_data["EID Date"] = eid_date

        # Append the extracted data to the results list
        combined_results.append(extracted_data)

# Convert the list of dictionaries into a DataFrame
final_df = pd.DataFrame(combined_results)

# Save the combined data to an Excel and CSV file
final_df.to_excel("Data_processing.xlsx", index=False)
final_df.to_csv("Data_processing.csv", index=False)

# Print the final combined data
print(final_df)
