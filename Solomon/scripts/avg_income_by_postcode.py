import pandas as pd

income_file_path = r"D:\Solomon\remaining_csv\England postcodes.csv"
population_file_path = r"D:\Solomon\remaining_csv\population_data.csv"
housing_file_path = r"D:\Solomon\census_data\census_data\ts_wise\Housing\TS054-Tenure\census2021-ts054-oa-summarized.csv"

# Load the data
df_income = pd.read_csv(income_file_path, low_memory=False)
df_population = pd.read_csv(population_file_path, low_memory=False)
df_housing = pd.read_csv(housing_file_path, low_memory=False)

# Extract postcode district from the income data
df_income['outcode'] = df_income['Postcode'].apply(lambda x: x.split()[0])

# Calculate average and median income by postcode district
average_income_by_district = df_income.groupby('outcode')['Average Income'].mean().round(2).reset_index()
median_income_by_district = df_income.groupby('outcode')['Average Income'].median().round(2).reset_index()

# Rename columns for clarity
average_income_by_district.rename(columns={'Average Income': 'Average Income'}, inplace=True)
median_income_by_district.rename(columns={'Average Income': 'Median Income'}, inplace=True)

# Merge average income, median income, and population data
merged_data = pd.merge(average_income_by_district, median_income_by_district, on='outcode')
merged_data = pd.merge(merged_data, df_population, on='outcode')
merged_data = pd.merge(merged_data,df_housing,on='outcode')

# Calculate per capita income
merged_data['Per Capita Income'] = (merged_data['Tenure of household: Total: All households']*merged_data['Average Income'] / df_population['population']).round(2)

final_data = merged_data[['outcode', 'Average Income', 'Median Income', 'Per Capita Income']]
# Save the result to a CSV file
final_data.to_csv('income_population_percapita.csv', index=False)

print("Average income, median income, and per capita income by postcode district saved to 'income_population_percapita.csv'")
