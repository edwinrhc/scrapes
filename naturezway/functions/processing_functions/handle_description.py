import pandas as pd
from functions.processing_functions.utils import (clean_text, extract_size_from_description, extratact_material_from_description, extract_volume_from_description, extract_product_value)

import params as params

# 1. Clean the description by removing
#    - special characters
#    - emojis
#    - extra spaces
#    - non-ASCII characters
def clean_description(input_file_path, output_file_path):
  # Load the CSV file
  products_df = pd.read_csv(input_file_path, keep_default_na=False)

  # Fill na values with empty strings
  products_df = products_df.fillna('')

  # Uncomment to remove the upc and manufacturerNumber columns
  products_df['upc'] = products_df['upc'].apply(lambda x: "")
  products_df['manufacturerNumber'] = products_df['upc'].apply(lambda x: "")

  # Clean the description
  products_df['description'] = products_df['description'].apply(clean_text)

  # Save the modified dataframe to a CSV file
  products_df.to_csv(output_file_path, index=False)
  print(f"Cleaned the description and saved to {output_file_path}")

# 2. Extract the size from the description
def extract_sizes(input_file_path, output_file_path):
  # Load the CSV file
  products_df = pd.read_csv(input_file_path, keep_default_na=False)

  # Extract the size from the description
  new_df = []
  for index, row in products_df.iterrows():
    new_row = extract_size_from_description(row)
    new_df.append(new_row)

  # Save the modified dataframe to a CSV file
  processed_df = pd.DataFrame(new_df)
  processed_df.to_csv(output_file_path, index=False)
  print(f"Extracted the size from the description and saved to {output_file_path}")

# 3. Extract the material from the description
def extract_material(input_file_path, output_file_path):
  # Load the CSV file
  products_df = pd.read_csv(input_file_path, keep_default_na=False)

  # Extract the material from the description
  new_df = []
  for index, row in products_df.iterrows():
    new_row = extratact_material_from_description(row)
    new_df.append(new_row)

  # Save the modified dataframe to a CSV file
  processed_df = pd.DataFrame(new_df)
  processed_df.to_csv(output_file_path, index=False)
  print(f"Extracted the material from the description and saved to {output_file_path}")

# 4. Extract the volume from the description
def extract_volume(input_file_path, output_file_path):
  # Load the CSV file
  products_df = pd.read_csv(input_file_path, keep_default_na=False)

  # Extract the volume from the description/title
  new_df = []
  for index, row in products_df.iterrows():
    new_row = extract_volume_from_description(row)
    new_df.append(new_row)

  # Save the modified dataframe to a CSV file
  processed_df = pd.DataFrame(new_df)
  processed_df.to_csv(output_file_path, index=False)
  print(f"Extracted the volume from the description/title and saved to {output_file_path}")

# 5. Extract the packSize from the description
def extract_pack_size():
  pass

# 6. Extract the productValue
def set_product_value(input_file_path, output_file_path):
  # Load the csv file
  products_df = pd.read_csv(input_file_path, keep_default_na=False)

  # Extract the product value
  new_df = []
  for index, row in products_df.iterrows():
    new_row = extract_product_value(row)
    new_df.append(new_row)

  # Save the modified dataframe to a CSV file
  processed_df = pd.DataFrame(new_df)
  processed_df.to_csv(output_file_path, index=False)
  print(f"Extracted the product value and saved to {output_file_path}")

# 7. Extract the color from the description
def extract_color():
  pass
