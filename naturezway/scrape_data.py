import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

import random

from functions.scraping_functions.collection import loop_collections_pages, get_collections_data
from functions.scraping_functions import products as products
from functions.processing_functions.handle_title import (get_model_from_title, get_package_from_title)
import params as params

# Set up options to run the driver without GUI
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
# chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
# chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems

# chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# chrome_options.add_argument("--disable-javascript")
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--ignore-ssl-errors')
# chrome_options.add_argument('--log-level=3') # Minimal logs in console (only fatal errors)

# Set up the driver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)

# Get & save the collections url and names
# collections = get_collections_data(driver, params.BASE_URL)
# print('Collections: ', collections)
# collection_df = pd.DataFrame(collections, columns=['url', 'name'])
# collection_df.to_csv(params.COLLECTIONS_PATH, index=False)

# collections = [{'name': 'Bath Tissue & Facial Tissue', 'url': 'https://naturezway.com/collections/bath-tissue'}, {'name': 'Paper Towels', 'url': 'https://naturezway.com/collections/paper-towels'}, {'name': 'Plates & Bowels', 'url': 'https://naturezway.com/collections/plates-bowels'}, {'name': 'Cutlery', 'url': 'https://naturezway.com/collections/cutlery'}, {'name': 'Napkins', 'url': 'https://naturezway.com/collections/napkins'}, {'name': 'Hot Cups', 'url': 'https://naturezway.com/collections/hot-and-cold-cups'}, {'name': 'Cold Cups', 'url': 'https://naturezway.com/collections/cold-cups'}, {'name': 'Straws', 'url': 'https://naturezway.com/collections/straws'}, {'name': 'To-Go Containers', 'url': 'https://naturezway.com/collections/to-go-containers'}, {'name': 'Food Cling Wrap', 'url': 'https://naturezway.com/collections/food-cling-wrap'}, {'name': 'Sponges & Cleaning Cloths', 'url': 'https://naturezway.com/collections/sponges-and-cleaning-cloths'}]

# Get the collection's products links
# all_products = []
# for collection in collections:
#   random_time = random.randint(params.MIN_COLLECTION_SLEEP, params.MAX_COLLECTION_SLEEP)
#   print(f'Waiting {random_time} seconds before scraping the next collection...')
#   time.sleep(random_time)
#   print('Scraping collection: ', collection['name'])
#   products_links = loop_collections_pages(driver, collection['url'], By.CLASS_NAME, 'product-card')

  # Get the products data
#   for product_link in products_links:
#     try:
#       product = products.get_product_data(driver, product_link, collection['name'])
#       all_products.append(product)
#     except Exception as e:
#       print('Error scraping product: ', product_link)
#       print('Error: ', e)
#       continue

# Close the driver
# print('Closing driver...')
# driver.quit()

# Save the products data
# products_df = pd.DataFrame(all_products, columns=params.HEADERS)
# file_path = 'scraped_data/products.csv'
# products_df.to_csv(file_path, index=False)
