import pandas as pd

file_path = r"D:\Solomon\Phase 1\Solomon\completed_csv\price_paid_data.csv"
temp_path = r"D:\Solomon\Phase 1\Solomon\completed_csv\test_property_data.csv"

data = pd.read_csv(file_path)

price_columns = ['Avg sold price (Detached)', 'Avg sold price (Semi-detached)', 
                 'Avg sold price (Terraced)', 'Avg sold price (Flat)']

data['Avg sold price'] = data[price_columns].median(axis=1).round(2)

final_csv = ['outcode', 'Avg sold price', 'Avg sold price (Detached)', 
                  'Avg sold price (Semi-detached)', 'Avg sold price (Terraced)', 
                  'Avg sold price (Flat)']

data.to_csv(temp_path,index=False,columns=final_csv)
