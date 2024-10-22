import pandas as pd
import os

def merge_csvs(csv_paths, common_column, output_path):
    if not csv_paths:
        print("No CSV files to merge.")
        return None
    
    # Load the first CSV to initialize the merging process
    merged_data = pd.read_csv(csv_paths[0])

    # Loop through the remaining CSV files and merge them
    for csv_file in csv_paths[1:]:
        print(f"Processing... {csv_file}")

        df = pd.read_csv(csv_file)

        merged_data = pd.merge(merged_data, df, on=common_column, how='outer')
    
    merged_data.fillna(0, inplace=True)

    merged_data.to_csv(output_path, index=False)
    
    print(f"All CSVs merged successfully and saved to {output_path}")
    
    return merged_data


# Example usage:
csv_folder = r"D:\Solomon\completed_csv" 
output_csv = r"D:\Solomon\merged_output.csv"  
common_column = "outcode" 

csv_files = [os.path.join(csv_folder, f) for f in os.listdir(csv_folder) if f.endswith('.csv')]

merged_df = merge_csvs(csv_files, common_column, output_csv)

