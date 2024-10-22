import pandas as pd

file_path = r"D:\Solomon\completed_csv\updated_rent_data.csv"
output_path = r"D:\Solomon\completed_csv\rent_data.csv"

data = pd.read_csv(file_path)

data['avg_gross_yield']= data['avg_gross_yield'].round(2)

# columns = ['Postcode','Avg asking rent(p/m)','Avg asking rent(1 bed)','Avg asking rent(2 beds)','Avg asking rent(3 beds)','Avg asking rent(4 beds)','Avg asking rent(5 beds)','avg_gross_yield']

data.to_csv(output_path,index=False)

print("Average sold prices calculated for each distinct outcode:")
