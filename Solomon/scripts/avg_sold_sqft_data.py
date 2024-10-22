import pandas as pd

floor_area = r"D:\Solomon\remaining_csv\floor_area_data.csv"
listing_data = r"D:\Solomon\completed_csv\property_data.csv"
sold_data = r"D:\Solomon\completed_csv\price_paid_data.csv"

df_floor = pd.read_csv(floor_area)
df_listing = pd.read_csv(listing_data)
df_sold = pd.read_csv(sold_data)

df_listing['Avg Listing per sqft'] = (df_listing['avg_asking_price'] / df_floor['avg_surface_area_ft2']).round(2)
df_sold['Avg Sold per sqft'] = (df_sold['Avg sold price'] / df_floor['avg_surface_area_ft2']).round(2)

merged_df = pd.merge(df_floor, df_listing[['outcode', 'Avg Listing per sqft']], on='outcode', how='left')
merged_df = pd.merge(merged_df, df_sold[['outcode', 'Avg Sold per sqft']], on='outcode', how='left')

# Verify that the columns exist in merged_df before selecting
print("Columns in merged_df:", merged_df.columns.tolist())

# Define the final columns for the output
columns = ['outcode', 'Avg Listing per sqft', 'Avg Sold per sqft']

# Check if the columns exist in the merged DataFrame
missing_columns = [col for col in columns if col not in merged_df.columns]
if missing_columns:
    print(f"Missing columns: {missing_columns}")
else:
    # Select the final columns
    final_df = merged_df[columns]

    # Save the result to a new CSV
    final_df.to_csv(r"D:\Solomon\completed_csv\final_property_data.csv", index=False)

    print("Data successfully processed and saved to 'final_property_data.csv'")
