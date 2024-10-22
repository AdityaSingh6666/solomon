import os
import requests
from parsel import Selector
import pandas as pd
import zipfile
import shutil

def process_oa_csv(ts_folder_path, ts_code, postcode_oa_file_path):
    for csv_filename in os.listdir(ts_folder_path):
        if "-oa.csv" in csv_filename:
            
            csv_file_path = os.path.join(ts_folder_path, csv_filename)
            
            file_size = os.path.getsize(csv_file_path)
            if file_size == 0:
                print(f"Skipping {csv_filename} as it is empty. No data found for {ts_code}")
                continue
            
            census_bulk_data_df = pd.read_csv(csv_file_path)
            
            postcode_with_oa = pd.read_csv(postcode_oa_file_path)
            
            merged_df = pd.merge(postcode_with_oa, census_bulk_data_df, on='geography code', how='inner')
            merged_df = merged_df.drop(columns=['date', 'geography'], errors='ignore')
            
            processed_csv_filename = csv_filename.replace('.csv', '-processed.csv')
            processed_csv_path = os.path.join(ts_folder_path, processed_csv_filename)
            merged_df.to_csv(processed_csv_path, index=False)
            
            shutil.copy(processed_csv_path, os.path.join(OUTPUT_CENSUS_DATA_FOLDER, ALL_CSV_FILES_PROCESSED_FOLDER, processed_csv_filename))
            
            summarize_csv_file(ts_folder_path, processed_csv_filename, ts_code)
            
            break

def summarize_csv_file(ts_folder_path, processed_csv_filename, ts_code):
    
    processed_csv_path = os.path.join(ts_folder_path, processed_csv_filename)
    df = pd.read_csv(processed_csv_path)
    
    df_summarized = df.groupby('outcode').sum().reset_index()
    summarized_csv_filename = processed_csv_filename.replace('-processed.csv', '-summarized.csv')
    
    summarized_csv_path = os.path.join(ts_folder_path, summarized_csv_filename)
    df_summarized.to_csv(summarized_csv_path, index=False)
    
    shutil.copy(summarized_csv_path, os.path.join(OUTPUT_CENSUS_DATA_FOLDER, ALL_CSV_FILES_SUMMARISED_FOLDER, summarized_csv_filename))

def cleanup_non_oa_files(ts_folder_path):
    for csv_filename in os.listdir(ts_folder_path):
        #check folder and remove all files except -oa.csv, -oa-processed.csv, -oa-summarized.csv
        if os.path.isfile(os.path.join(ts_folder_path, csv_filename)):
            
            if not ("-oa.csv" in csv_filename or "-oa-processed.csv" in csv_filename or "-oa-summarized.csv" in csv_filename):
                os.remove(os.path.join(ts_folder_path, csv_filename))
                # print(f"Removed {csv_filename}")


POSTCODE_OA_FILE_NAME = 'postcodes_demo_with_outcodes.csv'
POSTCODE_OA_FILE_PATH = os.path.join(os.getcwd(), POSTCODE_OA_FILE_NAME)

OUTPUT_CENSUS_DATA_FOLDER = 'census_data'
ALL_CSV_FILES_PROCESSED_FOLDER = 'all_csv_files_processed'
ALL_CSV_FILES_SUMMARISED_FOLDER = 'all_csv_files_summarised'
TS_WISE_FOLDER = os.path.join(OUTPUT_CENSUS_DATA_FOLDER, 'ts_wise')

os.makedirs(OUTPUT_CENSUS_DATA_FOLDER, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_CENSUS_DATA_FOLDER, ALL_CSV_FILES_PROCESSED_FOLDER), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_CENSUS_DATA_FOLDER, ALL_CSV_FILES_SUMMARISED_FOLDER), exist_ok=True)
os.makedirs(TS_WISE_FOLDER, exist_ok=True)

url = "https://www.nomisweb.co.uk/sources/census_2021_bulk"
response = requests.get(url)

html = response.text
parsed_html = Selector(text=html)

header_folders = parsed_html.xpath('//tr[td/h2]')

for header_folder in header_folders:
    
    header_folder_name = header_folder.xpath('.//h2/text()').get()
    header_folder_path = os.path.join(TS_WISE_FOLDER, header_folder_name)
    os.makedirs(header_folder_path, exist_ok=True)
    
    print("-" * 50)
    print(f"Processing {header_folder_name}")
    
    current_row = header_folder.xpath('./following-sibling::tr[1]')
    
    while current_row:
        if current_row.xpath('.//h2'):
            break
        
        ts_code = current_row.xpath('.//td[1]/strong/text()').get()
        if ts_code is None or "ASP" in ts_code:
            break
        
        description = current_row.xpath('.//td[2]/text()').get()
        output_link = current_row.xpath('.//td[3]//a/@href').get()
        
        ts_folder_path = os.path.join(header_folder_path, f"{ts_code}-{description}")
        os.makedirs(ts_folder_path, exist_ok=True)
        
        print(f"Processing {ts_code} - {description} under {header_folder_name}")
        # print(f"Output link: {output_link}")
        
        if output_link:
            output_url = f"https://www.nomisweb.co.uk{output_link}"
            output_file_path = os.path.join(ts_folder_path, f"{ts_code}_output.zip")
            
            response = requests.get(output_url)
            with open(output_file_path, 'wb') as file:
                file.write(response.content)
            
            try:
                with zipfile.ZipFile(output_file_path, 'r') as zip_ref:
                    zip_ref.extractall(ts_folder_path)
            except zipfile.BadZipFile:
                print(f"Damaged/ Unknown format ZIP file found for {ts_code}. Skipping...")
                os.remove(output_file_path)
                break
            
            process_oa_csv(ts_folder_path, ts_code, POSTCODE_OA_FILE_PATH)
            os.remove(output_file_path)
            cleanup_non_oa_files(ts_folder_path)

        current_row = current_row.xpath('./following-sibling::tr[1]')

print("All files processed and summarized successfully.")
