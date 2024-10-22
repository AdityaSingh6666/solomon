import pandas as pd

file_path = r"D:\Solomon\remaining_csv\final_property_data.csv"

data = pd.read_csv(file_path)

data.columns = data.columns.str.strip()

print(data.columns)

avg_prices = data.groupby(['postcode', 'property_type']).agg({
    'price_paid': 'median'
}).reset_index()

avg_prices_pivot = avg_prices.pivot(index='postcode', columns='property_type', values='price_paid').reset_index()

# Dynamically rename columns based on the property types present
expected_columns = {
    'D': 'Avg sold price (Detached)',
    'S': 'Avg sold price (Semi-detached)',
    'T': 'Avg sold price (Terraced)',
    'F': 'Avg sold price (Flat)'
}

# Rename the columns in the pivot table to the more descriptive names
avg_prices_pivot.rename(columns=expected_columns, inplace=True)

# Calculate overall average price per postcode (ignoring property type)
overall_avg_prices = data.groupby('postcode')['price_paid'].mean().reset_index()
overall_avg_prices.rename(columns={'price_paid': 'Avg sold price'}, inplace=True)

# Merge overall average prices with the pivoted property type averages
result = pd.merge(overall_avg_prices, avg_prices_pivot, on='postcode', how='left')

# Round all price columns to 2 decimal places
price_columns = ['Avg sold price', 'Avg sold price (Detached)', 
                 'Avg sold price (Semi-detached)', 'Avg sold price (Terraced)', 
                 'Avg sold price (Flat)']
result[price_columns] = result[price_columns].round(2)

# Save the result to a new CSV
result_columns = ['postcode', 'Avg sold price', 'Avg sold price (Detached)', 
                  'Avg sold price (Semi-detached)', 'Avg sold price (Terraced)', 
                  'Avg sold price (Flat)']
result.to_csv(r"D:\Solomon\completed_csv\final_property_data.csv", index=False, columns=result_columns)

print("Final CSV created.")

