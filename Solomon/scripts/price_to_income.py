import pandas as pd

avg_income = r"D:\Solomon\remaining_csv\average_income_by_postcode_district.csv"
avg_sold_price = r"D:\Solomon\completed_csv\price_paid_data.csv"
avg_rent_price = r"D:\Solomon\completed_csv\rent_data.csv"

final_csv_path = r"D:\Solomon\completed_csv\price_to_income_data.csv"

df_income = pd.read_csv(avg_income)
df_sold_price = pd.read_csv(avg_sold_price)
df_rent_price = pd.read_csv(avg_rent_price)

df_income['Average Income'] = pd.to_numeric(df_income['Average Income'], errors='coerce')
df_sold_price['Avg sold price'] = pd.to_numeric(df_sold_price['Avg sold price'], errors='coerce')
df_rent_price['Avg asking rent(p/m)'] = pd.to_numeric(df_rent_price['Avg asking rent(p/m)'], errors='coerce')

merged_df = df_income.merge(df_sold_price[['outcode', 'Avg sold price']], on='outcode', how='left')
merged_df = merged_df.merge(df_rent_price[['outcode', 'Avg asking rent(p/m)']], on='outcode', how='left')

merged_df['Price to Income'] = ((merged_df['Avg sold price'] / merged_df['Average Income']) * 100).round(2)
merged_df['Rent to Income'] = ((merged_df['Avg asking rent(p/m)'] / merged_df['Average Income']) * 100).round(2)

final_df = merged_df[['outcode', 'Price to Income', 'Rent to Income']]

final_df.to_csv(final_csv_path, index=False)
