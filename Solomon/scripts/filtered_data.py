import pandas as pd 
import csv

input_csv = r"C:\Users\aadit\OneDrive\Desktop\Solomon\England_postcodes_filtered.csv"
output_csv = r"C:\Users\aadit\OneDrive\Desktop\Solomon\filtered.csv"

# Specify the columns you want to keep
columns_to_keep = [
    'Postcode', 
    'District Code', 
    'Region', 
    'County',  
    'Local authority',
    'District', 'Ward',
]

# Read the CSV file
df = pd.read_csv(input_csv)

# Check if all the required columns are in the dataframe
missing_columns = [col for col in columns_to_keep if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing columns in the input CSV: {', '.join(missing_columns)}")

# Select only the specified columns
df_filtered = df[columns_to_keep]

# Write the filtered data to a new CSV file
df_filtered.to_csv(output_csv, index=False)

print(f"Filtered data has been saved to {output_csv}")

