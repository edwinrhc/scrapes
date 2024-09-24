"""Import the necessary libraries"""
import sys
sys.path.append('/home/hjmacaya/code/hjmacaya/python-projects/lilo/scrapers/lilo-scrapers/eco-quality')
import pandas as pd
import functions.processing.utils as ut



# Read the csv
products_df = pd.read_csv('ecoquality_products_v9.csv', keep_default_na=False, low_memory=False)

# Loop through the rows
total_products = len(products_df)
for index, row in products_df.iterrows():

    print(f"Processing product {index}/{total_products}")

    # Check if it has volume
    if row['volumeOZ'] == "":

        # Extract volume from title
        volume = ut.extract_volume_from_title(row['metaTitle'])
        row['volumeOZ'] = volume

        if volume != "":
            print(f"Volume extracted: {volume}")

    else:
        print(f"Product {index} already has volume")


    print('\n')

# Save the csv
products_df.to_csv('ecoquality_products_v10.csv', index=False)
