import pandas as pd

# File path
deprivation_data_csv = r"D:\Solomon\census_data\census_data\ts_wise\Demography and migration\TS011-Households by deprivation dimensions\census2021-ts011-oa-summarized.csv"
final_csv_path = r"D:\Solomon\completed_csv\poverty_data.csv"

# Load the data
df = pd.read_csv(deprivation_data_csv)

# Column names in the CSV
columns = {
    'Household deprivation: Total: All households; measures: Value': 'total_households',
    'Household deprivation: Household is not deprived in any dimension; measures: Value': 'not_deprived',
    'Household deprivation: Household is deprived in one dimension; measures: Value': 'deprived_one',
    'Household deprivation: Household is deprived in two dimensions; measures: Value': 'deprived_two',
    'Household deprivation: Household is deprived in three dimensions; measures: Value': 'deprived_three',
    'Household deprivation: Household is deprived in four dimensions; measures: Value': 'deprived_four',
}

# Rename columns for clarity
df.rename(columns=columns, inplace=True)

# Calculate the number of households deprived in at least one dimension
df['deprived_one_or_more'] = df['deprived_one'] + df['deprived_two'] + df['deprived_three'] + df['deprived_four']

# Calculate poverty percentage
df['poverty_pct'] = (df['deprived_one_or_more'] / df['total_households'] * 100).round(2)

# Select only the required columns
final_data = df[['outcode', 'total_households','poverty_pct']]

# Save the final DataFrame to a CSV file
final_data.to_csv(final_csv_path, index=False)

print(f'Poverty data saved to {final_csv_path} successfully')
