import pandas as pd

# Load the CSV file
file_path = 'new1.csv'
df = pd.read_csv(file_path)

# Remove consecutive duplicate 'Update Time' entries
df_cleaned = df[df['Update Time'] != df['Update Time'].shift()]

# Save the cleaned dataframe to a new CSV file
output_path = 'cleaned_data.csv'
df_cleaned.to_csv(output_path, index=False)

print(f"Cleaned data saved to {output_path}")
