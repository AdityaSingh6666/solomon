import pandas as pd

# Paths to input and output data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\completed_csv\household_composition_data.csv"
household_composition_csv_path =  r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Demography and migration\TS003-Household composition\census2021-ts003-oa-summarized.csv"

df = pd.read_csv(f'{household_composition_csv_path}')
print(df.columns)

column_mapping = {
    'Household composition: Total; measures: Value' : 'Total households',
    'Household composition: One person household; measures: Value' : 'One Person household',
    'Household composition: Single family household; measures: Value' : 'Single family Household',
    'Household composition: Other household types; measures: Value' : 'Other household type',
}

# Load only the required columns from the CSV (including 'outcode')
required_columns = ['outcode'] + list(column_mapping.keys())

try:
    df = pd.read_csv(household_composition_csv_path, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {household_composition_csv_path}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Rename the columns in one step
df.rename(columns=column_mapping, inplace=True)

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Household data saved successfully to {final_csv_path}")

