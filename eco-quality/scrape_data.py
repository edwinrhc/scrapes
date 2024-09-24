from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time

import parameters.paths as paths
import parameters.products as ppr

from functions.scraping.collections import (get_collections, get_product_links)
from functions.scraping.products import (get_product_variants)
from functions.printing import (print_collection, print_product)
from functions.utils import (search_index, save_product_in_csv, set_starting_point, search_collection_index)

###################### DRIVER CONFIGURATION ######################
# Set up options to run the driver in headless mode
print("Setting up driver...")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems

chrome_options.add_experimental_option(
    "prefs",
    {"profile.managed_default_content_settings.images": 2}
    )
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--log-level=3') # Minimal logs in console (only fatal errors)

# Set up the driver
print("Connecting driver'0s service")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Finish setting up driver")
##################################################################

#################### GET COLLECTION DATA #########################
# Set initial time
# collection_init_time = time.time()

### ONLINE ALTERNATIVE: Get & save the collections data from website
# collection = get_collections(driver, paths.BASE_URL, True)
# collection_df = pd.DataFrame(
#     collection,
#     columns=['category', 'subcategory', 'sub_subcategory', 'name', 'filename', 'url']
#     )
# collection_df.to_csv(paths.COLLECTION_CSV_PATH, index=False)
# print_collection(collection)

### OFFLINE ALTERNATIVE: Get collection from CSV
collection_df = pd.read_csv(paths.COLLECTION_CSV_PATH, keep_default_na=False)
collection = collection_df.to_dict('records')
# print_collection(collection)

# Set the duration
# collection_duration = time.time() - collection_init_time
# print(f"Collection duration: {collection_duration} seconds")
##################################################################

#################### SEARCH INDEX COLLEC #########################
# last_index_visited = search_index(collection, 'name', 'Education School Supplies')
##################################################################

################## GET PRODUCT LINKS #############################
# Set initial time
# products_links_init_time = time.time()

# all_product_links = []
# for i in range(last_index_visited, len(collection)):
#     print(f"Getting product links for {collection[i]['name']}...")
#     product_links = get_product_links(driver, collection[i], all_product_links)
#     print(f"Found {len(product_links)} product links")

# Set the duration
# products_links_duration = time.time() - products_links_init_time
# print(f"Products links duration: {products_links_duration} seconds")

##################################################################

################### GET PRODUCT DATA #############################
# products = get_product_variants(
#     driver,
#     "https://ecoqualityinc.com/collections/freezers/products/refrigerator-freezer-thermometer-2-7-8",
#     collection[0],
#     False
#     )
# for product in products:
#     save_product_in_csv(f"data/scraped/products/{collection[0]['filename']}_products.csv", product)


############## CHECKPOINT #############
# Disposable Tableware and index 36
# #3 Disposable Microwavable Kraft Brown Folded Paper Take-Out Containers 66oz

category_index = 94
# category_index = 0
start_time = time.time()
for i, c in enumerate(collection[category_index:]):
    # 1. Open the product links CSV of the category
    try:
        products_links_df = pd.read_csv(f"data/scraped/{c['filename']}_products_links.csv")
        products_links = products_links_df.to_dict('records')
        print("\n")
        print("#" * 50)
        print(f"Getting products from category {c['name']} and index {category_index + i}...")
        print("#" * 50)
        print("\n")

        # 2. Check if there is a specific product to start from
        products_links, product_index = set_starting_point(
            'Fancy Disposable Gold Plastic Knives Extra Heavyweight Glamour Collection',
            products_links
            )

        # 3. Iterate over the links and get the data
        category_products = []
        for product_link in products_links:

            # Extract the product data
            print(f"Getting product data for {product_link['name']}")
            products = get_product_variants(driver, product_link['url'], c, False)

            # Save the product in a CSV
            for product in products:
                save_product_in_csv(f"data/scraped/products/{c['filename']}_products.csv", product)
                category_products.append(product)
            product_index += 1

    except FileNotFoundError:
        print(f"No products links found for category {c['name']}")
durantion_time = time.time() - start_time
print(f"Duration: {(durantion_time / 60) / 60} hours")
##################################################################

# product_df = pd.read_csv(f"data/scraped/products/Takeout_Containers_products.csv", keep_default_na=False)
# product_df.to_excel(f"data/scraped/products/Takeout_Containers_products.xlsx", index=False)

# Close the driver
print('Closing driver...')
driver.quit()
