import pandas as pd

# Paths to input and output data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\completed_csv\accomadation_type_data.csv"
accomadation_type_csv_path =  r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Housing\TS044-Accommodation type\census2021-ts044-oa-summarized.csv"

# df = pd.read_csv(f'{accomadation_type_csv_path}')
# print(df.columns)
# Define column mappings for renaming
column_mapping = {
    'Accommodation type: Total: All households' : 'total_households',
    'Accommodation type: Detached' : 'Detached' , 
    'Accommodation type: Semi-detached' : 'Semi-Detached',
    'Accommodation type: Terraced' : 'Terraced',
    'Accommodation type: In a purpose-built block of flats or tenement' : 'Flat'
}

# Load only the required columns from the CSV (including 'outcode')
required_columns = ['outcode'] + list(column_mapping.keys())

try:
    df = pd.read_csv(accomadation_type_csv_path, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {accomadation_type_csv_path}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Rename the columns in one step
df.rename(columns=column_mapping, inplace=True)

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Housing data saved successfully to {final_csv_path}")

