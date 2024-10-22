import pandas as pd

# Paths to input and output data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\completed_csv\housing_data.csv"
housing_csv_path =  r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Housing\TS054-Tenure\census2021-ts054-oa-summarized.csv"

# Define column mappings for renaming
column_mapping = {
    'Tenure of household: Total: All households': 'housing_units',
    'Tenure of household: Owned: Owns outright': 'owns_outright',
    'Tenure of household: Owned: Owns with a mortgage or loan': 'own_with_mortgage',
    'Tenure of household: Private rented': 'private_rent',
    'Tenure of household: Social rented': 'social_rent',
    'Tenure of household: Lives rent free': 'rent_free',
    'Tenure of household: Shared ownership': 'shared_ownership'
}

# Load only the required columns from the CSV (including 'outcode')
required_columns = ['outcode'] + list(column_mapping.keys())

try:
    df = pd.read_csv(housing_csv_path, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {housing_csv_path}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Rename the columns in one step
df.rename(columns=column_mapping, inplace=True)

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Housing data saved successfully to {final_csv_path}")

