import pandas as pd
import params as params
from functions.processing_functions.utils import (extract_model_name, standardize_model_name, assign_best_fit_model, get_package)

# Function to extract model names from product titles
def get_model_from_title(input_file_path, output_file_path):
    # Load the CSV file
    products_df = pd.read_csv(input_file_path, keep_default_na=False)

    # Apply the model name extraction logic to each title
    products_df['model_name'] = products_df.apply(lambda row: extract_model_name(row['title'], params.MODEL_KEYWORDS), axis=1)

    # Standardize model names
    products_df['model_name'] = products_df['model_name'].apply(standardize_model_name)

    # Assuming the 'vendorCategory.0' and model names are already processed
    category_to_models = products_df.groupby('vendorCategory.0')['model_name'].unique().to_dict()
    products_df['model'] = products_df.apply(lambda row: assign_best_fit_model(row['title'], category_to_models.get(row['vendorCategory.0'], [])), axis=1)

    # Remove the model_name column
    products_df = products_df.drop(columns=['model_name'])

    # Save the modified dataframe to a CSV file
    products_df.to_csv(output_file_path, index=False)

    print(f"Set model name to products correctly and saved to {output_file_path}")

# Function to extract package details from product title
def get_package_from_title(input_file_path, output_file_path):
    # Load the CSV file
    products_df = pd.read_csv(input_file_path, keep_default_na=False)

    # Fill NaN values with empty strings
    products_df = products_df.fillna('')

    # Define a regex pattern to match the packaging details in the title
    pattern = r"\((\d+)(\s*|-)(ROLLS|ROLL|PACK|PACKS|BOX|LID PACK|CUPS)[^\)]*\)\s*"

    # Apply the processing to each row
    new_data = []
    for index, row in products_df.iterrows():
        processed_title = get_package(row['title'], row, pattern)
        row['title'] = processed_title
        new_data.append(row)

    # Create a new DataFrame with the updated data
    processed_df = pd.DataFrame(new_data)

    # Save the processed DataFrame to a new CSV file
    processed_df.to_csv(output_file_path, index=False)
    print(f"Extracted package details from product titles and saved to {output_file_path}")

# Function to remove the pending "()" spec from title
def remove_pending_spec(input_file_path, output_file_path):
    # Load the CSV file
    products_df = pd.read_csv(input_file_path, keep_default_na=False)

    # Fill NaN values with empty strings
    products_df = products_df.fillna('')

    # Remove the pending "()" spec from title
    products_df['title'] = products_df['title'].str.replace(r"\(.*?\)", "", regex=True)

    # Save the modified dataframe to a CSV file
    products_df.to_csv(output_file_path, index=False)
    print(f"Removed the pending '()' spec from title and saved to {output_file_path}")
