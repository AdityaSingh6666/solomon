import pandas as pd

file_path = r"D:\Solomon\census_data\census_data\ts_wise\Work and Travel\TS066-Economic activity status\census2021-ts066-oa-summarized.csv"
final_csv_path = r"D:\Solomon\completed_csv\employment_data.csv"

column_mapping = {
    'Economic activity status: Economically active (excluding full-time students):In employment' :'In_Employment',  
    'Economic activity status: Economically active (excluding full-time students): Unemployed' : 'Unemployed',
    'Economic activity status: Economically inactive: Retired' : 'Retired',
}

required_columns = ['outcode'] + list(column_mapping.keys()) + ['Economic activity status: Economically active (excluding full-time students)' ]

df_emp = pd.read_csv(file_path,usecols=required_columns)

df_emp['Unemployment_pct'] = ((df_emp['Economic activity status: Economically active (excluding full-time students): Unemployed']/ df_emp['Economic activity status: Economically active (excluding full-time students)'])*100).round(2)

df_emp.rename(columns=column_mapping, inplace=True)

columns_order = ['outcode','In_Employment','Unemployed','Unemployment_pct','Retired']

df_emp = df_emp.reindex(columns = columns_order)
df_emp.to_csv(final_csv_path,index=False)

print(f"Employment data saved successfully to {final_csv_path}")
