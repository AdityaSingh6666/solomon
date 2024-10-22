import pandas as pd
import json

json_data = r"C:\Users\aadit\OneDrive\Desktop\planning_applications_28-09-2024.json"
final_csv_path = r"D:\Solomon\completed_csv\planning_application.csv"

# Load the JSON data
with open(json_data, 'r') as f:
    data = json.load(f)

applications = data

# Dictionary to store data
postcode_data = {}

# Iterate through the applications
for app in applications:
    postcode = app.get('postcode', None)
    app_state = app.get('app_state', None)

    # Skip if postcode is missing
    if not postcode:
        continue

    # Initialize or update postcode entry
    if postcode not in postcode_data:
        postcode_data[postcode] = {'total_applications': 0, 'successful_applications': 0}

    # Increment total applications
    postcode_data[postcode]['total_applications'] += 1

    # Increment successful applications if 'Permitted'
    if app_state == 'Permitted':
        postcode_data[postcode]['successful_applications'] += 1

# Create a DataFrame from the dictionary
result_df = pd.DataFrame.from_dict(postcode_data, orient='index').reset_index()
result_df.columns = ['postcode', 'total_applications', 'successful_applications']

# Extract the outcode (first part of the postcode)
result_df['Outcode'] = result_df['postcode'].apply(lambda x: x.split()[0])

# Group by outcode and aggregate total and successful applications
grouped_result_df = result_df.groupby('Outcode').agg({
    'total_applications': 'sum',
    'successful_applications': 'sum'
}).reset_index()

# Calculate success rate and round to 2 decimal places
grouped_result_df['success_rate'] = (grouped_result_df['successful_applications'] / grouped_result_df['total_applications'] * 100).round(2).fillna(0)

# Save the result to a CSV file
grouped_result_df.to_csv(final_csv_path, index=False)

print(f"Data written to {final_csv_path}")
