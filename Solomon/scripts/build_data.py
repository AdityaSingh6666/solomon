import pandas as pd

build_type = r"D:\Solomon\remaining_csv\build_median_sold_prices.csv"
floor_area = r"D:\Solomon\remaining_csv\floor_area_data.csv"
final_csv_path = r"D:\Solomon\completed_csv\avg_sqft_sold_new_old.csv"

df_build = pd.read_csv(build_type)
df_floor = pd.read_csv(floor_area)

# # Extract outcode from postcode
# data['outcode'] = data['postcode'].str.split().str[0]

# # Calculate median price for new builds
# new_build_median = data[data['new_build'] == 'Y'].groupby('outcode')['price_paid'].median().reset_index()

# new_build_median.columns = ['outcode', 'new_build_median']

# # Calculate median price for old builds
# old_build_median = data[data['new_build'] == 'N'].groupby('outcode')['price_paid'].median().reset_index()
# old_build_median.columns = ['outcode', 'old_build_median']

# # Merge the results
# merged_data = pd.merge(new_build_median, old_build_median, on='outcode', how='outer')
merged_data = pd.merge(df_build,df_floor,on='outcode',how = 'left')

merged_data['new_build_median'] = merged_data['new_build_median'].fillna(0)
merged_data['old_build_median'] = merged_data['old_build_median'].fillna(0)
merged_data = merged_data.dropna(subset=['avg_surface_area_ft2'])
merged_data['Avg sold per sqft.(New)'] = merged_data['new_build_median'] / merged_data['avg_surface_area_ft2']

# Calculate Avg sold per sqft. for old builds
merged_data['Avg sold per sqft.(Old)'] = merged_data['old_build_median'] / merged_data['avg_surface_area_ft2']

# Optionally, round to 2 decimal places for readability
merged_data['Avg sold per sqft.(New)'] = merged_data['Avg sold per sqft.(New)'].round(2)
merged_data['Avg sold per sqft.(Old)'] = merged_data['Avg sold per sqft.(Old)'].round(2)

# Save the final result to CSV
merged_data.to_csv('avg_sold_per_sqft.csv', index=False)

columns = ['outcode','Avg sold per sqft.(New)','Avg sold per sqft.(Old)']

merged_data.to_csv(final_csv_path,index=False,columns = columns)

print(f'Data saved successfully at {final_csv_path}')