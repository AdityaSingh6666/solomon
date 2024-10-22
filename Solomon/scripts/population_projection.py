import pandas as pd

# Load the CSV file
file_path = r"C:\Solomon\remaining_csv\population_projection_2050.csv"
output_file_path = r"D:\Solomon\completed_csv\population_projection.csv"

df = pd.read_csv(file_path)

df['Change 2000-2010 (%)'] = (((df['2010'] - df['2000']) / df['2000']) * 100).round(2)
df['Change 2010-2020 (%)'] = (((df['2020'] - df['2010']) / df['2010']) * 100).round(2)
df['Change 2020-2030 (%)'] = (((df['2030'] - df['2020']) / df['2020']) * 100).round(2)

columns = ['CODE','2011','2021','2030','2050','Change 2000-2010 (%)','Change 2010-2020 (%)','Change 2020-2030 (%)']

df.to_csv(output_file_path, index=False,columns = columns)

print(f"Percentage changes saved to {output_file_path}")
