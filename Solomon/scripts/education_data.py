import pandas as pd

# Paths to input data
final_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\education_data.csv"

education_csv_path = r"C:\Users\aadit\OneDrive\Desktop\Solomon\census_data\census_data\ts_wise\Education\TS067-Highest level of qualification\census2021-ts067-oa-summarized.csv"

columns = ['outcode','edu_att_pop_16_plus','edu_att_no_diploma','edu_att_high_school' ,'edu_att_some_college','edu_att_bachelors' ,'edu_att_graduate']

df = pd.read_csv(f'{education_csv_path}')

selected_columns = ['outcode', 'geography code', 'postcodes',
       'Highest level of qualification: Total: All usual residents aged 16 years and over',
       'Highest level of qualification: No qualifications',
       'Highest level of qualification: Level 1 and entry level qualifications',
       'Highest level of qualification: Level 2 qualifications',
       'Highest level of qualification: Apprenticeship',
       'Highest level of qualification: Level 3 qualifications',
       'Highest level of qualification: Level 4 qualifications and above',
       'Highest level of qualification: Other qualifications']

# Drop the unnecessary columns
df = df[selected_columns].drop(columns=['geography code', 'postcodes','Highest level of qualification: Apprenticeship','Highest level of qualification: Other qualifications'])

# Rename columns to match the final column names
df.columns = columns

df['edu_att_no_diploma'] = ((df['edu_att_no_diploma'] / df['edu_att_pop_16_plus']) * 100).round(2).astype(str) + "%"
df['edu_att_high_school'] = ((df['edu_att_high_school'] / df['edu_att_pop_16_plus']) * 100).round(2).astype(str) + "%"
df['edu_att_some_college'] = ((df['edu_att_some_college'] / df['edu_att_pop_16_plus']) * 100).round(2).astype(str) + "%"
df['edu_att_bachelors'] = ((df['edu_att_bachelors'] / df['edu_att_pop_16_plus']) * 100).round(2).astype(str) + "%"
df['edu_att_graduate'] = ((df['edu_att_graduate'] / df['edu_att_pop_16_plus']) * 100).round(2).astype(str) + "%"

# Save the result to the final CSV file
df.to_csv(final_csv_path, index=False)

print(f"Education data with percentages saved successfully to {final_csv_path}")
