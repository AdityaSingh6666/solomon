import pandas as pd

# Paths to input and output data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\completed_csv\relationship_status.csv"
relationship_status_csv_path =  r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Demography and migration\TS002-Legal partnership status\census2021-ts002-oa-summarized.csv"

df = pd.read_csv(f'{relationship_status_csv_path}')
print(df.columns)

column_mapping = {
    'Marital and civil partnership status: Never married and never registered a civil partnership; measures: Value': 'Single',
    'Marital and civil partnership status: Married or in a registered civil partnership: Married; measures: Value': 'Married',
    'Marital and civil partnership status: Separated, but still legally married or still legally in a civil partnership; measures: Value': 'Seperated',
    'Marital and civil partnership status: Widowed or surviving civil partnership partner: Widowed; measures: Value' : 'Widowed',
    'Marital and civil partnership status: Divorced or civil partnership dissolved: Divorced; measures: Value': 'Divorced' 
}

# Load only the required columns from the CSV (including 'outcode')
required_columns = ['outcode'] + list(column_mapping.keys())

try:
    df = pd.read_csv(relationship_status_csv_path, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {relationship_status_csv_path}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Rename the columns in one step
df.rename(columns=column_mapping, inplace=True)

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Relationship data saved successfully to {final_csv_path}")

