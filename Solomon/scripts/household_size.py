import pandas as pd

# Paths to input and output data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\completed_csv\household_size_data.csv"
household_size_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Demography and migration\TS017-Household size\census2021-ts017-oa-summarized.csv"

# Column mapping
column_mapping = {
    'Household size: 1 person in household; measures: Value': '1 person',
    'Household size: 2 people in household; measures: Value': '2 people',
    'Household size: 3 people in household; measures: Value': '3 people',
    'Household size: 4 people in household; measures: Value': '4 people'
}

# Columns to load
required_columns = ['outcode'] + list(column_mapping.keys()) + [
    'Household size: 5 people in household; measures: Value',
    'Household size: 6 people in household; measures: Value',
    'Household size: 7 people in household; measures: Value',
    'Household size: 8 or more people in household; measures: Value'
]

# Load the required columns from the CSV
try:
    df = pd.read_csv(household_size_csv_path, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {household_size_csv_path}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Rename columns
df.rename(columns=column_mapping, inplace=True)

# Combine columns to create '5 person plus'
df['5 person plus'] = df[
    ['Household size: 5 people in household; measures: Value',
     'Household size: 6 people in household; measures: Value',
     'Household size: 7 people in household; measures: Value',
     'Household size: 8 or more people in household; measures: Value']
].sum(axis=1)

# Drop the original 5+ columns if not needed
df.drop(columns=[
    'Household size: 5 people in household; measures: Value',
    'Household size: 6 people in household; measures: Value',
    'Household size: 7 people in household; measures: Value',
    'Household size: 8 or more people in household; measures: Value'
], inplace=True)

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Household size data saved successfully to {final_csv_path}")
