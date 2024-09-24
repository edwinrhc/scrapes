"""Functions to process the product's data"""
import ast
import functions.processing_utils as fpu
import pandas as pd

def set_unchanged_columns(row, product_dict):
    """Function to set the unchanged field"""
    product_dict['url'] = row['url']
    product_dict['metaTitle'] = row['title']
    # product_dict['title'] = row['type']
    product_dict['metaDescription'] = row['description']
    product_dict['description'] = row['description']
    product_dict['brand'] = row['brand']
    product_dict['ingredients'] = row['ingredients']
    product_dict['productValues'] = row['product_values']
    product_dict['images'] = []
    product_dict['specifications'] = []
    product_dict['options'] = []

def save_upcs(row, product_dict):
    """Function to save the upcs"""
    product_dict['upc'] = row['box_upc']
    if row['retail_upc'] != "":
        product_dict['specifications'].append((
            'Retail UPC', row['retail_upc']
        ))
    if row['unit_upc'] != "":
        product_dict['specifications'].append((
            'Unit UPC', row['unit_upc']
        ))

def save_id(row, product_dict):
    """Function to save the id"""
    product_dict['specifications'].append((
        'L&E Bottling ID', row['id']
    ))

def process_stock(row, product_dict):
    """Function to process the stock"""

    # Get if the product is available
    stock = row['stock'].lower()
    if 'available' in stock:
        product_dict['availableForSale'] = True
    else:
        product_dict['availableForSale'] = False

    # Get the inventory
    inventory = stock.split(" ")[0]
    if inventory != "out":
        product_dict['totalInventory'] = inventory
    else:
        product_dict['totalInventory'] = 0

def process_price(row, product_dict):
    """Function to process the price"""
    price = row['price'].split("/")[0]
    price = price.replace("$", "")
    product_dict['price'] = price
    product_dict['ourCost'] = price
    product_dict['productMinOrderPrice'] = price

def save_constant_fields(product_dict):
    """Function to save the fields that are constant"""
    product_dict['vendor'] = "L&E Bottling"
    product_dict['manufacturerName'] = "L&E Bottling"
    product_dict['canCustomize'] = False
    product_dict['productMinOrderCases'] = 1


def process_images(row, product_dict):
    """Function to process the images"""
    images = ast.literal_eval(row['images'])
    if len(images) == 1:
        if 'not-available' in images[0]:
            product_dict['images'] = ''
        else:
            product_dict['images'] = images
    else:
        product_dict['images'] = images

def extract_pack_case_size(row, product_dict):
    """Function to extract the pack and case size"""
    title = row['title']
    brand = row['brand']
    product_dict['caseSize'] = fpu.get_case_size(title)
    product_dict['packSize'] = fpu.get_pack_size(title)
    if fpu.is_only_ct(title):
        product_dict['packSize'] = fpu.get_only_ct(title)
        product_dict['caseSize'] = 1
    elif fpu.is_other_pack_size(title):
        product_dict['packSize'] = fpu.get_other_pack_size(title)
        product_dict['caseSize'] = 1
    elif "CT BOX" in title:
        product_dict['packSize'] = fpu.get_ct_box_size(title)
    elif "FLTERS" in title:
        product_dict['caseSize'] = 1
        product_dict['packSize'] = fpu.get_filters_pack_size(title)
    elif brand == "CUPS/LIDS/SUP" and product_dict['packSize'] == "":
        product_dict['packSize'] = fpu.get_parenthesis_pack_size(title)


def process_volume(row, product_dict):
    """Function to process the volume"""
    product_dict['volume'] = fpu.extract_volume(row['title'])
    if product_dict['volume'] == "" and row['volume'] != "":
        product_dict['volume'] = fpu.format_volume(row['volume'])

def extract_capacity(row, product_dict):
    """Function to extract the capacity of the product"""
    capacity = fpu.extract_capacity(row['title'])
    if capacity != "":
        product_dict['specifications'].append(('Capacity', capacity))

def extract_size(row, product_dict):
    """Function to extract the size of the product"""
    size = fpu.extract_size(row['title'])
    if size != "":
        product_dict['specifications'].append(('Size', size))
        product_dict['size'] = f"{size} in"
        product_dict['productLength'] = f"{size} in"


def process_title(row, product_dict):
    """Function to process the title"""
    title = row['title']

    # Remove caseSize
    title = fpu.remove_case_size(title)

    # Remove packSize
    title = fpu.remove_pack_size(title)

    # Remove other packsizes
    title = fpu.remove_only_ct(title)
    title = fpu.remove_other_pack_size(title)

    # Remove CT BOX pack size
    title = fpu.remove_ct_box_size(title)

    # Remove flters pack size
    title = fpu.remove_flters_pack_size(title)

    # Remove volume
    title = fpu.remove_volume(title)

    # Remove capacity
    title = fpu.remove_capacity(title)

    # Remove the size
    title = fpu.remove_size(title)

    # Remove special characters
    title = fpu.remove_acronyms(title)

    # Remove the extra numbers
    title = fpu.remove_extra_numbers(title)


    # Final adjustments
    title = title.replace("  ", " ").replace("   ", " ")
    title = title.strip()
    product_dict['title'] = title
    if "flters" in product_dict['metaTitle'].lower():
        print(f"TTTLE: {title} \nMETA: {product_dict['metaTitle']}\n")

def fix_options_and_images(input_path, output_path):
    """Function to fix the options and images"""

    # Open the products CSV
    products_df = pd.read_csv(input_path, keep_default_na=False)

    products_v2 = []
    for index, row in products_df.iterrows():

        # Check if the product has image
        if row['images'] == '':
            row['availableForSale'] = False

        # Save caseSize in options
        row['options'] = ast.literal_eval(row['options'])
        if row['caseSize'] != '':
            row['options'].append((
                'Case size', row['caseSize']
            ))

        # Save packSize in options
        if row['packSize'] != '':
            row['options'].append((
                'Pack size', row['packSize']
            ))

        # Save Volume in options
        if row['volume'] != '':
            row['options'].append((
                'Volume', row['volume']
            ))

        # Save SIze in options
        if row['size'] != '':
            row['options'].append((
                'Size', row['size']
            ))

        new_row = row
        products_v2.append(new_row)

    # Save products_df to a new CSV
    products_df_v2 = pd.DataFrame(products_v2)
    products_df_v2.to_csv(output_path, index=False)
