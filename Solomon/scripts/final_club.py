import pandas as pd

# Define file paths
input_csv = r"C:\Users\aadit\OneDrive\Desktop\Solomon\filtered.csv"
output_csv = r"C:\Users\aadit\OneDrive\Desktop\Solomon\populated_data.csv"

# Read the CSV file with detailed postcodes
df = pd.read_csv(input_csv)

# Extract base postcodes (first part before space)
df['Base Postcode'] = df['Postcode'].str.split(' ',n=1).str[0]

# Group by base postcode and combine values
# You can use aggregation functions to combine the data
df_grouped = df.groupby('Base Postcode').agg({
    'District Code': lambda x: ', '.join(x.dropna().astype(str).unique()),
    'Region': lambda x: ', '.join(x.dropna().astype(str).unique()),
    'County': lambda x: ', '.join(x.dropna().astype(str).unique()),
    'Local authority': lambda x: ', '.join(x.dropna().astype(str).unique()),
    'District': lambda x: ', '.join(x.dropna().astype(str).unique()),
    'Ward': lambda x: ', '.join(x.dropna().astype(str).unique()),
}).reset_index()

# Rename columns if needed (for clarity or format)
df_grouped.rename(columns={'Base Postcode': 'postcode',
                           'District Code':'district_code',
                           'Region':'region',
                           'County':'county_name',
                           'Local Authority':'local_authority',
                           'District Name':'District_name',
                           'Ward':'ward_name'}, inplace=True)

# Save the results to a new CSV file
df_grouped.to_csv(output_csv, index=False)

print(f"Clubbed postcodes have been saved to {output_csv}")
