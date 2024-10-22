import json
import csv

# Function to clean and format currency values
def clean_currency(value):
    if value:
        return value.replace('£', '').replace(',', '')  # Remove currency symbol and commas
    return None

# Function to remove BOM from dictionary keys
def remove_bom_from_keys(d):
    if isinstance(d, dict):
        new_dict = {}
        for k, v in d.items():
            new_key = k.lstrip('\ufeff')  # Remove BOM character
            new_dict[new_key] = remove_bom_from_keys(v)
        return new_dict
    elif isinstance(d, list):
        return [remove_bom_from_keys(i) for i in d]
    else:
        return d

# The provided JSON file path
json_file_path = r"D:\Solomon\JSON\sales_data_16-09-2024.json"

# Load JSON data into a Python list
with open(json_file_path, 'r', encoding='utf-8-sig') as file:
    data_list = json.load(file)

# Prepare CSV file
csv_file_path = r"D:\Solomon\completed_csv\property_data.csv"
header = ['Postcode', 'avg_asking_price', 'avg_asking_price_1bed', 'avg_asking_price_2beds', 'avg_asking_price_3beds', 'avg_asking_price_4beds', 'avg_asking_price_5beds', 'days_on_market','Sales per month','Sale/List Ratio']

# Open CSV file for writing
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # Writing the header

    # Process each item in the data list
    for data_dict in data_list:
        data_dict = remove_bom_from_keys(data_dict)  # Remove BOM from keys
        
        # Extract required fields
        postcode = data_dict.get('location', None)
        avg_asking_price = clean_currency(data_dict.get('avg_price', None))

        # Parse the JSON string for property prices
        property_prices_str = data_dict.get('Property Prices by Number of Bedrooms', "[]")
        try:
            property_prices = json.loads(property_prices_str)  # Convert JSON string to list
        except json.JSONDecodeError:
            property_prices = []  # Handle the case where parsing fails
        
        total_properties = float(data_dict.get('total_properties_for_sale', None).replace(',','').strip())
        avg_ToM_days = float(data_dict.get('avg_ToM_unsold_properties', None).replace('days','').strip())

        if total_properties and avg_ToM_days:
            try:
                avg_ToM_months = float(avg_ToM_days) / 30  # Convert days to months
                sales_per_month = round(float(total_properties) / avg_ToM_months, 2)
            except ValueError:
                sales_per_month = None
        else:
            sales_per_month = None

        overall_time_to_sell_str = data_dict.get('Overall Time to Sell', '[]')
        try:
            overall_time_to_sell = json.loads(overall_time_to_sell_str)
            properties_to_sell = overall_time_to_sell[0].get('total_properties', '0')
        except (json.JSONDecodeError, IndexError):
            properties_to_sell = '0'

        # Calculate sale_to_list_ratio
        properties_to_sell = float(properties_to_sell)
        if total_properties and properties_to_sell:
            try:
                sale_to_list_ratio = round(float(properties_to_sell)*100 / total_properties, 2)
            except ValueError:
                sale_to_list_ratio = None
        else:
            sale_to_list_ratio = None
        # Extract and clean average prices for different bedroom counts
        avg_asking_price_1bed = clean_currency(property_prices[0]['avg_price']) if len(property_prices) > 0 else None
        avg_asking_price_2beds = clean_currency(property_prices[1]['avg_price']) if len(property_prices) > 1 else None
        avg_asking_price_3beds = clean_currency(property_prices[2]['avg_price']) if len(property_prices) > 2 else None
        avg_asking_price_4beds = clean_currency(property_prices[3]['avg_price']) if len(property_prices) > 3 else None
        avg_asking_price_5beds = clean_currency(property_prices[4]['avg_price']) if len(property_prices) > 4 else None

        days_on_market = data_dict.get('avg_ToM_unsold_properties', None)

        # Write data row to CSV
        data_row = [postcode, avg_asking_price, avg_asking_price_1bed, avg_asking_price_2beds, avg_asking_price_3beds, avg_asking_price_4beds, avg_asking_price_5beds, days_on_market,sales_per_month,sale_to_list_ratio]
        writer.writerow(data_row)

print(f"CSV file created: {csv_file_path}")
