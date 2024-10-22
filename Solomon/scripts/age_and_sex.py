import pandas as pd

# Paths to input data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\age_and_sex_data.csv"

sex_data_csv = r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Demography and migration\TS008-Sex\census2021-ts008-oa-summarized.csv"

age_data_csv = r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Demography and migration\TS007A-Age by five-year age bands\census2021-ts007a-oa-summarized.csv"

# Columns for the new dataframe
columns = ['outcode', 'age_total', 'sex_female', 'sex_male', 'age_4_under', 'age_5_9', 'age_10_14', 
           'age_15_19', 'age_20_24', 'age_25_29', 'age_30_34', 'age_35_39', 'age_40_44', 'age_45_49','age_50_54','age_55_59','age_60_64','age_65_69','age_70_74','age_75_79','age_80_84', 'age_85_plus', 'median_age']

# Load the population data and population density data
df1 = pd.read_csv(sex_data_csv)
df2 = pd.read_csv(age_data_csv)

# Merge on the common column
merged_df = pd.merge(df1, df2, on='outcode')

# Select specific columns from both
selected_columns = merged_df[[ 'outcode', 'Sex: All persons; measures: Value','Sex: Female; measures: Value','Sex: Male; measures: Value', 'Age: Aged 4 years and under','Age: Aged 5 to 9 years','Age: Aged 10 to 14 years','Age: Aged 15 to 19 years','Age: Aged 20 to 24 years','Age: Aged 25 to 29 years','Age: Aged 30 to 34 years','Age: Aged 35 to 39 years','Age: Aged 40 to 44 years','Age: Aged 45 to 49 years','Age: Aged 50 to 54 years','Age: Aged 55 to 59 years','Age: Aged 60 to 64 years','Age: Aged 65 to 69 years','Age: Aged 70 to 74 years','Age: Aged 75 to 79 years','Age: Aged 80 to 84 years','Age: Aged 85 years and over']]

# Age group ranges and their approximate midpoints
age_groups = {
    'Age: Aged 4 years and under': 2,        # Midpoint of 0-4
    'Age: Aged 5 to 9 years': 7,             # Midpoint of 5-9
    'Age: Aged 10 to 14 years': 12,          # Midpoint of 10-14
    'Age: Aged 15 to 19 years': 17,          # Midpoint of 15-19
    'Age: Aged 20 to 24 years': 22,          # Midpoint of 20-24
    'Age: Aged 25 to 29 years': 27,          # Midpoint of 25-29
    'Age: Aged 30 to 34 years': 32,          # Midpoint of 30-34
    'Age: Aged 35 to 39 years': 37,          # Midpoint of 35-39
    'Age: Aged 40 to 44 years': 42,          # Midpoint of 40-44
    'Age: Aged 45 to 49 years': 47,          # Midpoint of 45-49
    'Age: Aged 50 to 54 years': 52,          # Midpoint of 50-54
    'Age: Aged 55 to 59 years': 57,          # Midpoint of 55-59
    'Age: Aged 60 to 64 years': 62,          # Midpoint of 60-64
    'Age: Aged 65 to 69 years': 67,          # Midpoint of 65-69
    'Age: Aged 70 to 74 years': 72,          # Midpoint of 70-74
    'Age: Aged 75 to 79 years': 77,          # Midpoint of 75-79
    'Age: Aged 80 to 84 years': 82,          # Midpoint of 80-84
    'Age: Aged 85 years and over': 90        # Midpoint of 85+
}


# Function to calculate the median age
def calculate_median_age(row):
    total_population = row[age_groups.keys()].sum()
    cumulative_population = 0
    
    for age_group, midpoint in age_groups.items():
        cumulative_population += row[age_group]
        if cumulative_population >= total_population / 2:
            return midpoint
    
    return None

# Add a new column for median age
selected_columns['median_age'] = selected_columns.apply(calculate_median_age, axis=1)

# Save the result to CSV
selected_columns.to_csv(f'{final_csv_path}', index=False)

print(f"Age and sex data with median age saved successfully to {final_csv_path}")
