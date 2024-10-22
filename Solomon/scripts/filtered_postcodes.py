import pandas as pd

file_path = r"C:\Solomon\remaining_csv\pop_2001_2011.csv"

df = pd.read_csv(file_path)

df['2000'] = pd.to_numeric(df['2000'].str.replace(',', ''),errors = 'coerce')
df['2010'] = pd.to_numeric(df['2010'].str.replace(',', ''),errors = 'coerce')
df['2011'] = pd.to_numeric(df['2011'].str.replace(',', ''),errors = 'coerce')

df.to_csv(file_path, index=False)

print(f"Filtered data saved to {file_path}")
