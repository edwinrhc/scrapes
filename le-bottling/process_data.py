"""Import the necessary libraries"""
import pandas as pd

import parameters.products as pprod
import parameters.paths as ppaths
import functions.processing as fp

# 1. Open the products CSVs and join them
products_df_1 = pd.read_csv('data/scraped/products_part_1.csv', keep_default_na=False)
products_df_2 = pd.read_csv('data/scraped/products_part_2.csv', keep_default_na=False)
products_df = pd.concat([products_df_1, products_df_2], ignore_index=True)
index_to_drop = products_df[products_df['url'] == 'https://apps.vtinfo.com/retailer-portal/13000/retailer/31336/items/detail/48852'].index
products_df.drop(index_to_drop, inplace=True)

# 2. Set the final df with columns
final_df = pd.DataFrame(columns=pprod.HEADERS)

# 3. Iterate over the products_df
for index, row in products_df.iterrows():

    # if index == 301:
    #     break

    # if 100 < index <= 200:

    # print(f"{index}. Processing product: {row['title']}")
    # print(f"URL: {row['url']} \n")

    # Init the product dict
    processed_product = {}
    for header in pprod.HEADERS:
        processed_product[header] = ""

    # 3.1. Set the unchanged fields
    fp.set_unchanged_columns(row, processed_product)

    # 3.2. Save the upcs
    fp.save_upcs(row, processed_product)

    # 3.3. Save the id
    fp.save_id(row, processed_product)

    # 3.4. Process stock
    fp.process_stock(row, processed_product)

    # 3.5. Process price
    fp.process_price(row, processed_product)

    # 3.6. Save the constant fields
    fp.save_constant_fields(processed_product)

    # 3.7. Process images
    fp.process_images(row, processed_product)

    # 3.8. Extract pack and case size
    fp.extract_pack_case_size(row, processed_product)

    # 3.9. Extract and process the volume
    fp.process_volume(row, processed_product)

    # 3.10. Extract the capacity
    fp.extract_capacity(row, processed_product)

    # 3.11. Extract the size
    fp.extract_size(row, processed_product)

    # 3.11. Process title
    fp.process_title(row, processed_product)

    # 3. Save the processed product
    final_df.loc[index] = processed_product


# 4. Save in csv and excel
final_df.to_csv(ppaths.FINAL_PRODUCTS_PATH, index=False)
final_df.to_excel(ppaths.FINAL_PRODUCTS_PATH_EXCEL, index=False)

# 5. Fix options and products without images
fp.fix_options_and_images(ppaths.FINAL_PRODUCTS_PATH, ppaths.FINAL_PRODUCTS_PATH)
