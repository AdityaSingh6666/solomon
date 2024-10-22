import pandas as pd
import logging

file_path = r"D:\Solomon\remaining_csv\pp-complete.csv"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

logging.info('Starting to read the CSV file')

df = pd.read_csv(file_path)
   
logging.info('CSV file read successfully')

# columns = ['data_id','price_paid','deed_date','postcode','property_type','new_build','estate_type','paon','saon','street','locality','town','district','county','transaction_category','transaction_category_duplicate']

# df.columns = columns

# logging.info('Columns assigned successfully')

# df.drop(['data_id','transaction_category_duplicate'],axis= 1, inplace = True)

# logging.info('Column "data_id" and "transaction_category_duplicate" dropped')
# df.sort_values(by='postcode',inplace =True)

# column_order = ['postcode'] + [col for col in df.columns if col != 'postcode']
# df = df[column_order]

df_filtered = df[df['postcode'].notna()]

df_filtered.to_csv(file_path,index=False)

logging.info(f"price_paid_csv sorted by postcode saved successfully at {file_path}")