import pandas as pd

file_path = r"D:\Solomon\remaining_csv\England postcodes.csv"

df = pd.read_csv(file_path)

filtered_data = df[df['In Use?'] == 'Yes']

result = filtered_data[['Postcode', 'Average Income']]

result.to_csv('filtered_postcode_income.csv', index=False)

print("Filtered data saved to 'filtered_postcode_income.csv'")
