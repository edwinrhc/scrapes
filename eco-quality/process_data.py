"""Import the necessary libraries"""
import pandas as pd
import functions.processing.handling_options as ho
import parameters.paths as paths

def process_data(read_path, save_path):

    # 0. Check the options
    try:
        print("All options before formatting\n")
        ho.print_all_available_options(read_path)
        print("\n")
    except Exception as e:
        print(f"Error printing available options: {e}")

    # 1. Remove unnecessary columns
    try:
        print("Removing unnecessary columns...")
        ho.remove_columns(
        read_path,
        save_path
        )
    except Exception as e:
        print(f"Error removing unnecessary columns: {e}")

    # 2. Handle the product's options
    try:
        print("Processing the options of the product...")
        ho.format_options(
        save_path,
        save_path
        )
    except Exception as e:
        print(f"Error processing the options of the product: {e}")

    # 3. Standarize the options values
    try:
        print("Standarizing the options values...")
        ho.standarize_options_values(
        save_path,
        save_path
        )
    except Exception as e:
        print(f"Error standarizing the options values: {e}")


    # 4. Extract the selected options of the product
    try:
        print("Extracting the selected options of the product...")
        ho.extract_selected_options(
        save_path,
        save_path
        )
    except Exception as e:
        print(f"Error extracting the selected options of the product: {e}")

    # 5. Extract product value
    try:
        print("Extracting the product value...")
        ho.get_product_values(
        save_path,
        save_path
        )
    except Exception as e:
        print(f"Error extracting the product value: {e}")

    # 6. Extract the number of rolls
    try:
        print("Extracting the number of rolls...")
        ho.extract_number_of_rolls(
        save_path,
        save_path
        )
    except Exception as e:
        print(f"Error extracting the number of rolls: {e}")

    try:
        print("Printing available options...")
        ho.print_all_available_options(save_path)
    except Exception as e:
        print(f"Error printing available options: {e}")

process_data(
    "data/scraped/products/Cannabis_Supplies_products.csv",
    "data/processed/Cannabis_Supplies_products_final.csv"
)

# collection_df = pd.read_csv(paths.COLLECTION_CSV_PATH, keep_default_na=False)
# collections = collection_df.to_dict('records')

# all_available_options = []
# for i, collection in enumerate(collections):
#     print(f"Processing data for collection {collection['name']}...")
#     process_data(
#         f"data/scraped/products/{collection['filename']}_products.csv",
#         f"data/processed/{collection['filename']}_products.csv"
#     )

#     if i == 11:
#         break



# # 3. Format the size of the product
# try:
#     print("Formatting the size of the product...")
#     ho.format_size(
#     "data/processed/Takeout_Containers_products.csv",
#     "data/processed/Takeout_Containers_products.csv"
#     )
# except Exception as e:
#     print(f"Error formatting the size of the product: {e}")
