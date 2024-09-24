import pandas as pd
import params as params

from functions.processing_functions.utils import (extract_number_of_plies, extract_number_of_rolls)

# Function to set the # of plies
def set_number_of_plies(input_file_path, output_file_path):
  # Load the CSV file
  products_df = pd.read_csv(input_file_path, keep_default_na=False)

  # Set the number of plies
  new_df = []
  for index, row in products_df.iterrows():
    new_row = extract_number_of_plies(row)
    new_df.append(new_row)

  # Save the modified dataframe to a CSV file
  products_df = pd.DataFrame(new_df)
  products_df.to_csv(output_file_path, index=False)
  print(f"Extracted the number of plies and saved to {output_file_path}")

# Function to set the number of rolls
def set_number_of_rolls(input_file_path, output_file_path_csv, output_file_path_xlsx):
  # Load the CSV file
  products_df = pd.read_csv(input_file_path, keep_default_na=False)

  # Set the number of rolls
  new_df = []
  for index, row in products_df.iterrows():
    new_row = extract_number_of_rolls(row)
    new_df.append(new_row)

  # Save the modified dataframe to a CSV file
  products_df = pd.DataFrame(new_df)
  products_df.to_csv(output_file_path_csv, index=False)
  products_df.to_excel(output_file_path_xlsx, index=False)
  print(f"Extracted the number of rolls and saved to {output_file_path_csv} \n")
