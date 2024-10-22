import pandas as pd

# Paths to input data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\population_data.csv"

population_csv = r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Demography and migration\TS001-Number of usual residents in households and communal establishments\census2021-ts001-oa-summarized.csv"

population_density = r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Demography and migration\TS006-Population density\census2021-ts006-oa-summarized.csv"

# Columns for the new dataframe
columns = ['outcode', 'most_current_pop_year', 'population', 'pop_dens_sq_km']

# Create an empty list to store rows
data = []

# Load the population data and population density data
df1 = pd.read_csv(population_csv)
df2 = pd.read_csv(population_density)

print(f"Number of rows in population data: {len(df1)}")
print(f"Number of rows in population density data: {len(df2)}")

# Debug: Checking column names in df1 and df2
print(f"df1 columns: {df1.columns}")
print(f"df2 columns: {df2.columns}")

# Iterate through each row of the population data and populate columns
for index, row in df1.iterrows():
    row_data = {}

    # Check if 'outcode' and 'population' columns exist in df1
    if 'outcode' in df1.columns and 'Residence type: Total; measures: Value' in df1.columns:
        # Extract the 'outcode' and 'population' from df1 (population data)
        row_data['outcode'] = row['outcode']
        row_data['population'] = row['Residence type: Total; measures: Value']
    else:
        print(f"Column names 'outcode' or 'population' not found in df1")
        continue
    # Set the current population year (e.g., 2021 for now)
    row_data['most_current_pop_year'] = 2021

    # Debug: Checking if outcode exists in population density data (df2)
    if row_data['outcode'] in df2['outcode'].values:
        row_data['pop_dens_sq_km'] = df2.loc[df2['outcode'] == row_data['outcode'], 'Population Density: Persons per square kilometre; measures: Value'].values[0]
    else:
        row_data['pop_dens_sq_km'] = None  # If no matching entry found in df2
        print(f"No matching outcode found for {row_data['outcode']} in population density data.")

    # Append the row data to the list
    data.append(row_data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data, columns=columns)

# Save the final DataFrame to a CSV file
df.to_csv(final_csv_path, index=False)

print(f"Populated CSV saved at {final_csv_path}")

# Residence type: Total; measures: Value,Residence type: Lives in a household; measures: Value
# Population Density: Persons per square kilometre; measures: Value