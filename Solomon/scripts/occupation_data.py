import pandas as pd

# Paths to input and output data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\completed_csv\occupation_data.csv"
occupation_csv_path =  r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Work and Travel\TS063-Occupation\census2021-ts063-oa-summarized.csv"

df = pd.read_csv(f'{occupation_csv_path}')
print(df.columns)
# Define column mappings for renaming
column_mapping = {
    'Occupation (current): 1. Managers, directors and senior officials' : 'Managers' ,
    'Occupation (current): 2. Professional occupations' : 'Professionals',
    'Occupation (current): 3. Associate professional and technical occupations' : 'Assosiates',
    'Occupation (current): 4. Administrative and secretarial occupations' : 'Administrative',
    'Occupation (current): 5. Skilled trades occupations' : 'Skilled Trades',
    'Occupation (current): 6. Caring, leisure and other service occupations' : 'Caring and Leisure',
    'Occupation (current): 7. Sales and customer service occupations' : 'Sales and customer Service',
    'Occupation (current): 8. Process, plant and machine operatives' : 'Process Plant & Machine',
    'Occupation (current): 9. Elementary occupations' : 'Elementry'
}

# # Load only the required columns from the CSV (including 'outcode')
required_columns = ['outcode'] + list(column_mapping.keys())

try:
    df = pd.read_csv(occupation_csv_path, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {occupation_csv_path}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Rename the columns in one step
df.rename(columns=column_mapping, inplace=True)

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Occupation data saved successfully to {final_csv_path}")

