import pandas as pd

# Updated list of counties
updated_counties = [
    "Somerset", "Bedfordshire", "Rutland", "Cambridgeshire", 
    "Cheshire", "City of London", "Cleveland", "Cumbria", "Derbyshire", 
    "Devon", "Cornwall", "Dorset", "County Durham", "Dyfed-Powys", "Essex", 
    "Gloucestershire", "Greater Manchester", "Gwent", "Hampshire", 
    "Hertfordshire", "East Riding of Yorkshire", "Kent", "Lancashire", 
    "Leicestershire", "Lincolnshire", "Merseyside", "Greater London", "Norfolk", 
    "North Yorkshire", "Northamptonshire", "Northumberland", "Nottinghamshire", 
    "Oxfordshire", "Tyne and Wear", "Shropshire", "Somerset", 
    "South Yorkshire", "Staffordshire", "Suffolk", "Surrey", 
    "West Sussex", "Warwickshire", "West Midlands", "West Yorkshire", 
    "Wiltshire", "Worcestershire"
]
file_path = r"D:\Solomon\remaining_csv\combined_county_crime_data.csv"

# Read your CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Check if 'county' column exists in the DataFrame
if 'County' in df.columns:
    # Replace the 'county' column with the updated list of counties
    df['County'] = updated_counties[:len(df)]  # Ensure it only replaces up to the length of your data
else:
    print("'county' column not found in the CSV file")

# Save the modified DataFrame to a new CSV file
df.to_csv('updated_file.csv', index=False)

print("County column updated and saved to 'updated_file.csv'.")
