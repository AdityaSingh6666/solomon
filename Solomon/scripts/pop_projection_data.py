import pandas as pd
import numpy as np

# Load the CSV file
file_path = r"C:\Solomon\remaining_csv\merged_population.csv"
df = pd.read_csv(file_path)

# Prepare the data for regression
years = np.array([2000, 2010, 2011, 2020, 2021, 2030, 2043])
projected_populations = []

for index, row in df.iterrows():
    # Extract the population data, converting to numeric
    y = pd.to_numeric(row[1:])  # Assuming the first column is 'CODE'
    
    # Calculate the mean of years and populations
    x_mean = np.mean(years)
    y_mean = np.mean(y)
    
    # Calculate the slope (m) and intercept (b) for the linear regression
    numerator = np.sum((years - x_mean) * (y - y_mean))
    denominator = np.sum((years - x_mean) ** 2)
    
    if denominator == 0:  # Avoid division by zero
        slope = 0
    else:
        slope = numerator / denominator
    
    intercept = y_mean - slope * x_mean
    
    # Predict for 2050
    projected_population_2050 = slope * 2050 + intercept
    projected_populations.append(projected_population_2050)

# Add projected populations to the DataFrame
df['2050'] = projected_populations

df['2050'] = df['2050'].round(2)
# Save the updated DataFrame to a new CSV file
output_file_path = r"C:\Solomon\remaining_csv\population_projection_2050.csv"
df.to_csv(output_file_path, index=False)

print(f"Projected populations saved to {output_file_path}")
