"""Import the necessary libraries"""
import pandas as pd

import functions.processing.utils as ut

def remove_columns(input_path, output_path):
    """Remove unnecessary columns"""

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Remove unnecessary columns
    df_columns = products_df.columns
    for col in df_columns:
        if "images" in col:
            col_splited = col.split(".")
            if int(col_splited[1]) > 6:
                products_df = products_df.drop(columns=[col])

    # 3. Save the new data
    products_df.to_csv(output_path, index=False)
    products_df.to_excel(output_path.replace(".csv", ".xlsx"), index=False)

def format_options(input_path, output_path):
    """Format the options of the product"""

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Format size/dimension from the product
    new_data = []
    for index, row in products_df.iterrows():
        new_row = ut.fromat_all_options(row)
        new_data.append(new_row)

    # 3. Save the new data
    new_products_df = pd.DataFrame(new_data)
    new_products_df.to_csv(output_path, index=False)
    new_products_df.to_excel(output_path.replace(".csv", ".xlsx"), index=False)

def extract_selected_options(input_path, output_path):
    """Extract the selected options of the product"""

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Extract selected options
    new_data = []
    for index, row in products_df.iterrows():
        new_row = ut.extract_selected_options(row)
        new_data.append(new_row)

    # 3. Save the new data
    new_products_df = pd.DataFrame(new_data)
    new_products_df.to_csv(output_path, index=False)
    new_products_df.to_excel(output_path.replace(".csv", ".xlsx"), index=False)

def standarize_options_values(input_path, output_path):
    """Function to standarize the options values"""

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Standarize the options values
    new_data = []
    for index, row in products_df.iterrows():
        new_row = ut.standarize_options_values(row)
        new_data.append(new_row)

    # 3. Save the new data
    new_products_df = pd.DataFrame(new_data)
    new_products_df.to_csv(output_path, index=False)
    new_products_df.to_excel(output_path.replace(".csv", ".xlsx"), index=False)

def get_product_values(input_path, output_path):
    """Extract the product value"""

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Get the values of the product
    new_data = []
    for index, row in products_df.iterrows():
        new_row = ut.extract_product_value(row)
        new_data.append(new_row)

    # 3. Save the new data
    new_products_df = pd.DataFrame(new_data)
    new_products_df.to_csv(output_path, index=False)
    new_products_df.to_excel(output_path.replace(".csv", ".xlsx"), index=False)

def format_size(input_path, output_path):
    """Format the size of product: L x W x H"""

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Format size/dimension from the product
    new_data = []
    for index, row in products_df.iterrows():
        new_row = ut.set_format_to_size(row)
        new_data.append(new_row)

    # 3. Save the new data
    new_products_df = pd.DataFrame(new_data)
    new_products_df.to_csv(output_path, index=False)
    new_products_df.to_excel(output_path.replace(".csv", ".xlsx"), index=False)

def extract_number_of_rolls(input_path, output_path):

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Extract the number of rolls
    new_data = []
    for index, row in products_df.iterrows():
        new_row = ut.extract_number_of_rolls(row)
        new_data.append(new_row)

    # 3. Save the new data
    new_products_df = pd.DataFrame(new_data)
    new_products_df.to_csv(output_path, index=False)
    new_products_df.to_excel(output_path.replace(".csv", ".xlsx"), index=False)

def print_all_available_options(input_path):
    """Print all the available options"""

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Get all the available options
    available_options = {}
    for index, row in products_df.iterrows():
        options = ut.get_available_options_v2(row)
        for option in options:
            if option not in available_options:
                available_options[option] = options[option]
            else:
                available_options[option] = available_options[option] + options[option]
                available_options[option] = list(set(available_options[option]))

    # 3. Print the available options
    for option in available_options:
        print(f"{option}: {available_options[option]} \n")

def get_all_available_options(input_path):
    """Print all the available options"""

    # 1. Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False)

    # 2. Get all the available options
    available_options = {}
    for index, row in products_df.iterrows():
        options = ut.get_available_options_v2(row)
        for option in options:
            if option not in available_options:
                available_options[option] = options[option]
            else:
                available_options[option] = available_options[option] + options[option]
                available_options[option] = list(set(available_options[option]))

    return available_options
