import pandas as pd

# Paths to input and output data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\completed_csv\health_data.csv"
health_data_csv_path =  r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Health\TS037-General health\census2021-ts037-oa-summarized.csv"

df = pd.read_csv(f'{health_data_csv_path}')
print(df.columns)

column_mapping = {
    'General health: Very good health': 'Very Good Health',
    'General health: Good health': 'Good Health',
    'General health: Fair health': 'Fair Health',
    'General health: Bad health' : 'Bad Health',
    'General health: Very bad health': 'Very Bad Health' 
}

# Load only the required columns from the CSV (including 'outcode')
required_columns = ['outcode'] + list(column_mapping.keys())

try:
    df = pd.read_csv(health_data_csv_path, usecols=required_columns)
except FileNotFoundError:
    print(f"Error: File not found at {health_data_csv_path}")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Rename the columns in one step
df.rename(columns=column_mapping, inplace=True)

# Save the updated DataFrame to a new CSV
df.to_csv(final_csv_path, index=False)

print(f"Health data saved successfully to {final_csv_path}")

