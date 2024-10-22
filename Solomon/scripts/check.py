import pandas as pd

temp_path = r"D:\Solomon\Phase 1\Solomon\completed_csv\test_property_data.csv"

data = pd.read_csv(temp_path)

price_columns = ['Avg sold price (Detached)', 'Avg sold price (Semi-detached)', 
                 'Avg sold price (Terraced)', 'Avg sold price (Flat)']

data['Avg sold price'] = data[price_columns].median(axis=1).round(2)

greater_than_million = data[price_columns].gt(1_000_000).any(axis=1)

if greater_than_million.any():
    print("Properties with avg price greater than 1 million:")
    print(len(data[greater_than_million]))
else:
    print("No properties with avg price greater than 1 million.")