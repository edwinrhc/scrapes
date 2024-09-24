"""Import the necessary libraries"""
import pandas as pd

def search_index(dict_list, key, value):
    """Function to search for index inside a list of dictionaries"""
    for i, element in enumerate(dict_list):
        if element[key] == value:
            return i
    return -1

# def search_index(dict_list, key, value):
#     """Function to search for index inside a list of dictionaries"""
#     for i in range(len(dict_list)):
#         if dict_list[i][key] == value:
#             return i
#     return -1

def save_product_in_csv(path, product_dict):
    """Function to save the product in a csv"""
    try:
        # Try to read the file
        product_df = pd.read_csv(path, low_memory=False)

        # Append the new data
        product_df.loc[len(product_df.index)] = product_dict

        # Save the file
        product_df.to_csv(path, index=False)
        product_df.to_excel(path.replace('.csv', '.xlsx'), index=False)

    except FileNotFoundError:
        # If the file does not exist, create it
        product_df = pd.DataFrame(
            [product_dict],
            columns=product_dict.keys()
        )
        product_df.to_csv(path, index=False)

def set_starting_point(product_name, products_links):
    """Function to set the products links start point"""
    start_index = 0
    if product_name != '':
        for index, product_link in enumerate(products_links):
            if product_link['name'] == product_name:
                start_index = index
                break

        if start_index != 0:
            products_links = products_links[start_index:]

    return products_links, start_index

def search_collection_index(collections, collection_name):
    """Function to search for the index of a collection"""
    for i, collection in enumerate(collections):
        if collection['name'] == collection_name:
            return i
    return -1
