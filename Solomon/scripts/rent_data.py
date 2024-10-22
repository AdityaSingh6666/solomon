import json
import csv

# Function to clean and format currency values
def clean_currency(value):
    if value:
        return value.replace('£', '').replace(',', '').replace('\u00a0','').replace('pcm','').strip()  # Remove currency symbol and commas
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
json_file_path = r"D:\Solomon\JSON\rent_data_18-09-2024.json"

# Load JSON data into a Python list
with open(json_file_path, 'r', encoding='utf-8-sig') as file:
    data_list = json.load(file)

# Prepare CSV file
csv_file_path = r"D:\Solomon\completed_csv\rent_data.csv"  # Modify the file path as needed
header = ['Postcode', 'Avg asking rent(p/m)', 'Avg asking rent(1 bed)', 'Avg asking rent(2 beds)', 'Avg asking rent(3 beds)', 'Avg asking rent(4 beds)', 'Avg asking rent(5 beds)']

# Open CSV file for writing
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # Writing the header

    # Process each item in the data list
    for data_dict in data_list:
        data_dict = remove_bom_from_keys(data_dict)  # Remove BOM from keys
        
        # Extract required fields
        postcode = data_dict.get('location', None)
        avg_asking_rent = clean_currency(data_dict.get('avg_rent', None))

        # Parse the JSON string for property prices
        property_prices_str = data_dict.get('Property Rents by Number of Bedrooms', "[]")
        try:
            property_prices = json.loads(property_prices_str)  # Convert JSON string to list
        except json.JSONDecodeError:
            property_prices = []  # Handle the case where parsing fails

        # Extract and clean average prices for different bedroom counts
        avg_asking_rent_1bed = clean_currency(property_prices[0]['avg_rent']) if len(property_prices) > 0 else None
        avg_asking_rent_2beds = clean_currency(property_prices[1]['avg_rent']) if len(property_prices) > 1 else None
        avg_asking_rent_3beds = clean_currency(property_prices[2]['avg_rent']) if len(property_prices) > 2 else None
        avg_asking_rent_4beds = clean_currency(property_prices[3]['avg_rent']) if len(property_prices) > 3 else None
        avg_asking_rent_5beds = clean_currency(property_prices[4]['avg_rent']) if len(property_prices) > 4 else None

        # Write data row to CSV
        data_row = [postcode, avg_asking_rent, avg_asking_rent_1bed, avg_asking_rent_2beds, avg_asking_rent_3beds, avg_asking_rent_4beds, avg_asking_rent_5beds]
        writer.writerow(data_row)

print(f"CSV file created: {csv_file_path}")
