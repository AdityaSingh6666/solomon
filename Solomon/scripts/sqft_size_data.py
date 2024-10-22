import pandas as pd

size_data = r"D:\Solomon\outcodes_crime_data_expanded.csv"
sold_price = r"D:\Solomon\completed_csv\population_growth_data.csv"

final_csv_path = r"D:\Solomon\completed_csv\crime_rate_data.csv"

df_size = pd.read_csv(size_data)
df_sold = pd.read_csv(sold_price)

merged_data = pd.merge(df_size,df_sold,on="outcode",how="left")

merged_data.fillna(0, inplace=True)

merged_data['Crime Rate'] = ((merged_data['Crime Data']*1000)/merged_data['2021']).round(2)

columns = ['outcode','Crime Rate']

merged_data.to_csv(final_csv_path,index=False,columns = columns)

print(f'Data saved successfully at {final_csv_path}')