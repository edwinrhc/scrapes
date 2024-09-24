"""Import the necessary libraries"""
import sys
sys.path.append('/home/hjmacaya/code/hjmacaya/python-projects/lilo/scrapers/lilo-scrapers/naturezway')

import pandas as pd
import functions.processing_functions.utils as ut

def set_data_new_template(input_path, output_path):
    """Function to set data into new template"""

    # Read the csv file
    products_df = pd.read_csv(input_path, keep_default_na=False, low_memory=False)

    # Loop through the rows in the dataframe
    new_data = []
    total_products = len(products_df)
    for index, row in products_df.iterrows():

        print(f"Processing product {index + 1} of {total_products}")

        ######## IMAGES ########
        row['images'] = ut.images_to_new_format(row)

        ######## SPECS #########
        row['specifications'] = ut.specs_to_new_format(row)

        ######## OPTS ##########
        row['options'] = ut.options_to_new_format(row)

        ###### PD VALUES #######
        row['productValues'] = ut.product_values_new_format(row)

        ######## VOLUME ########
        row['volume'] = row['volumeOz']

        # Append the row to the new data
        new_data.append(row)

    # Create new DataFrame
    new_products_df = pd.DataFrame(new_data)

    # Change columns names
    new_products_df.rename(columns={'feerPerRoll': 'feetPerRoll'}, inplace=True)

    # Remove old columns
    for col in new_products_df.columns:
        if 'images.' in col or 'specs.' in col or 'option.' in col or 'productValue.' in col:
            new_products_df = new_products_df.drop(columns=[col])
        if 'volumeOZ' in col or 'volumeML' in col or 'volumeOz' in col or 'volumeMl' in col:
            new_products_df = new_products_df.drop(columns=[col])

    # Save the new DataFrame to a new CSV file
    new_products_df.to_csv(output_path, index=False)
