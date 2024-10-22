import pandas as pd

# Sample data (replace this with your actual dataset)
data =  r"C:\Solomon\remaining_csv\interpolated_data_with_outcode.csv"
output_dir = r"C:\Solomon\remaining_csv\capital_growth_rates.csv"

df = pd.read_csv(data)

# Function to calculate capital growth from a base year
def calculate_growth(base_year, target_year, base_price, target_price):
    if pd.notnull(base_price) and pd.notnull(target_price):
        return round(((base_price - target_price) / target_price) * 100, 2)
    else:
        return None

# Initialize a list to store the results
results = []

# Loop through each outcode and calculate the growth rates using 2024 as the base year
for outcode, group in df.groupby('outcode'):
    base_price = group.loc[group['Year'] == 2024, 'price_paid'].values[0]

    # Get the prices for 1 year, 3 years, 5 years, and 10 years ago
    price_1yr = group.loc[group['Year'] == 2023, 'price_paid'].values[0] if 2023 in group['Year'].values else None
    price_3yr = group.loc[group['Year'] == 2021, 'price_paid'].values[0] if 2021 in group['Year'].values else None
    price_5yr = group.loc[group['Year'] == 2019, 'price_paid'].values[0] if 2019 in group['Year'].values else None
    price_10yr = group.loc[group['Year'] == 2014, 'price_paid'].values[0] if 2014 in group['Year'].values else None

    # Calculate the growth rates
    growth_1yr = calculate_growth(base_price, price_1yr, base_price, price_1yr)
    growth_3yr = calculate_growth(base_price, price_3yr, base_price, price_3yr)
    growth_5yr = calculate_growth(base_price, price_5yr, base_price, price_5yr)
    growth_10yr = calculate_growth(base_price, price_10yr, base_price, price_10yr)

    # Append the result to the list
    results.append({
        'outcode': outcode,
        'base_year': 2024,
        '1_yr_growth': growth_1yr,
        '3_yr_growth': growth_3yr,
        '5_yr_growth': growth_5yr,
        '10_yr_growth': growth_10yr
    })

# Create a dataframe from the results
growth_df = pd.DataFrame(results)

# Save to CSV
growth_df.to_csv(output_dir, index=False)

print(f"Summary of capital growth rates saved to {output_dir}")
