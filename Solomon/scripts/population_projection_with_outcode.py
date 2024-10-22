import pandas as pd

file_path = r"D:\Solomon\remaining_csv\final_populated_data.csv"
pop_path = r"D:\Solomon\completed_csv\population_projection.csv"

df_outcode = pd.read_csv(file_path)  # Contains 'outcode' and 'district_code'
df_population = pd.read_csv(pop_path)  # Contains 'district_code' and population projection data

# Step 1: Split multiple district codes into separate rows
df_outcode_expanded = df_outcode.assign(district_code=df_outcode['district_code'].str.split(',')).explode('district_code')
df_outcode_expanded['district_code'] = df_outcode_expanded['district_code'].str.strip()  # Remove extra spaces

# Step 2: Merge the outcode DataFrame with the population data on 'district_code'
merged_df = pd.merge(df_outcode_expanded, df_population, on='district_code', how='left')

# Step 3: Group by 'outcode' and aggregate population projection data (summing population projections if necessary)
# Replace 'population_column' with the actual column name(s) for population projections
grouped_df = merged_df.groupby('outcode').agg({'2011': 'median',
                                               '2021': 'median',
                                               '2030': 'median',
                                               '2050': 'median',
                                               'Change 2000-2010 (%)' : 'median',
                                               'Change 2010-2020 (%)' : 'median',
                                               'Change 2020-2030 (%)' : 'median'
                                               }).round(2).reset_index()

columns = ['outcode','2011','2021','2030','2050','Change 2000-2010 (%)','Change 2010-2020 (%)','Change 2020-2030 (%)']

grouped_df.to_csv('merged_outcode_population.csv', index=False,columns = columns)

print("Merge and aggregation complete. File saved as 'merged_outcode_population.csv'.")
