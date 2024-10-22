import pandas as pd

# Sample data
file_path = r"D:\Solomon\remaining_csv\planning_applications_by_postcode.csv"
output_file_path = r"D:\Solomon\completed_csv\planning_application.csv"

# Create a DataFrame
df = pd.read_csv(file_path)

df['Outcode'] = df['postcode'].apply(lambda x: x.split()[0])

# Group by outcode and aggregate
grouped_df = df.groupby('Outcode').agg({
    'total_applications': 'sum',
    'successful_applications': 'sum'
}).reset_index()

# Calculate success rate
grouped_df['success_rate'] = ((grouped_df['successful_applications'] / grouped_df['total_applications']).fillna(0) * 100).round(2)

grouped_df.to_csv(output_file_path,index=False)

print(f'Data saved successfully at {output_file_path}')