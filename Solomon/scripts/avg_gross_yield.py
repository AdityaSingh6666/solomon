import pandas as pd

rent_data = r"D:\Solomon\completed_csv\rent_data.csv"
property_data = r"D:\Solomon\completed_csv\property_data.csv"
final_csv_path = r"D:\Solomon\completed_csv\rent_data.csv"

# Load the CSV files
df_rent = pd.read_csv(rent_data)
df_property = pd.read_csv(property_data)

df_merged = pd.merge(df_rent, df_property, on='Postcode')

final_merged = df_merged[['Postcode','Avg asking rent(p/m)','Avg asking rent(1 bed)','Avg asking rent(2 beds)','Avg asking rent(3 beds)','Avg asking rent(4 beds)','Avg asking rent(5 beds)']].copy()

df_property.loc[:,'avg_asking_price'] = pd.to_numeric(df_property['avg_asking_price'], errors='coerce')
final_merged.loc[:,'Avg asking rent(p/m)'] = pd.to_numeric(final_merged['Avg asking rent(p/m)'], errors='coerce')

final_merged.loc[:,'avg_gross_yield'] = ((final_merged['Avg asking rent(p/m)'] / df_merged['avg_asking_price']) * 1200).round(2)

final_merged.to_csv(final_csv_path, index=False, float_format="%.2f")

print(f"Rent Data data saved to {final_csv_path}")


