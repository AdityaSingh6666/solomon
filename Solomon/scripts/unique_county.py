import pandas as pd

file_path = r"D:\Solomon\remaining_csv\final_populated_data.csv"

df = pd.read_csv(file_path)

unique_counties = df['county_name'].unique()

# Convert to list if needed
unique_counties_list = unique_counties.tolist()

print(len(unique_counties_list))
print(unique_counties_list)
