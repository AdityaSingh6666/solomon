import pandas as pd

# Paths to input and output data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\completed_csv\religion_data.csv"
religion_data_csv_path =  r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Ethnicity, Identity, Language and Religion\TS030-Religion\census2021-ts030-oa-summarized.csv"

column_mapping = {
    'Religion: Christian' : 'Christian',
    'Religion: Muslim' : 'Muslim',
    'Religion: Hindu' : 'Hindu',
    'Religion: Buddhist' : 'Buddhist',
    'Religion: Not answered' : 'None' 
}

# Load only the required columns from the CSV (including 'outcode')
required_columns = ['outcode','Religion: Other religion','Religion: Jewish', 'Religion: Sikh'] + list(column_mapping.keys())

try:
    df = pd.read_csv(religion_data_csv_path, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {religion_data_csv_path}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Rename the columns in one step
df.rename(columns=column_mapping, inplace=True)

df['Others'] = df[['Religion: Other religion','Religion: Jewish', 'Religion: Sikh']].sum(axis=1)

# Drop the original 5+ columns if not needed
df.drop(columns=['Religion: Jewish','Religion: Sikh','Religion: Other religion'], inplace=True)

columns_order = [col for col in df.columns if col != 'None'] + ['None']
df = df[columns_order]

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Religion data saved successfully to {final_csv_path}")

