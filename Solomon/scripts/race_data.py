import pandas as pd

ethnic_data_csv = r"D:\Solomon\census_data\census_data\ts_wise\Ethnicity, Identity, Language and Religion\TS021-Ethnic group\census2021-ts021-oa-summarized.csv"
final_csv_path = r"D:\Solomon\completed_csv\ethnic_data.csv"

df = pd.read_csv(ethnic_data_csv)

print(df.columns)

column_mapping = {
    'Ethnic group: Total: All usual residents' : 'race_ethnicity_total',
    'Ethnic group: White' : 'race_ethnicity_white',
    'Ethnic group: Black, Black British, Black Welsh, Caribbean or African' : 'race_ethnicity_black',
    'Ethnic group: Asian, Asian British or Asian Welsh' : 'race_ethnicity_asian',
    'Ethnic group: Other ethnic group' : 'race_ethnicity_other',
    'Ethnic group: Mixed or Multiple ethnic groups' : 'race_ethnicity_two_or_more',
}

# # Load only the required columns from the CSV (including 'outcode')
required_columns = ['outcode'] + list(column_mapping.keys())

try:
    df = pd.read_csv(ethnic_data_csv, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {ethnic_data_csv}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

df.rename(columns=column_mapping, inplace=True)

# Reorder columns to match the order in column_mapping
ordered_columns = ['outcode'] + list(column_mapping.values())
df = df[ordered_columns]

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Ethnic data saved successfully to {final_csv_path}")