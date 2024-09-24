""" Import the necessary libraries """
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import os
from dotenv import load_dotenv
import time
import pandas as pd

import functions.scraping as sf
import parameters.products as pprod
import parameters.paths as ppaths

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
chrome_options.add_argument('----window-size=1920,1080') # Screen size to 1920x1080

# Set up the driver
print("Connecting driver's service")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
print("Finish setting up driver")
##################################################################



#################### LOG IN TO THE WEBSITE #######################
# Load the login page
page_loaded = sf.get_login(driver)

# Load the credentials
load_dotenv()
username = os.getenv('VENDOR_MAIL')
password = os.getenv('VENDOR_PASSWORD')

# Log in to the website
print("Logging in...")
logged_in = sf.user_login(driver, username, password) if page_loaded else False
if logged_in:
    print("Logged in successfully")
##################################################################



#################### GET PRODUCTS LINKS #########################
# # Set initial time
# start_time = time.time()

# # Get the products
# if logged_in:

#     # Get products page
#     time.sleep(10)
#     products_page_loaded = sf.get_products_page(driver)
#     if products_page_loaded:

#         # Get products links
#         all_products_links = sf.get_all_products_links(driver)
#         print("\n All products links: ")
#         print(all_products_links)
#         print("\n")

#     else:
#         print("Fail to get products page")

# final_time = time.time()
# print(f"Time taken: {final_time - start_time}")
##################################################################



#################### GET PRODUCTS DATA ###########################
# Get the links from csv
product_links = sf.get_products_links_from_csv()

product_df = pd.DataFrame(columns=pprod.PRODUCT_COLUMNS)
if logged_in:
    for index, link in enumerate(product_links[760:]):

        new_index = index + 760

        full_link = ppaths.LANDING_BASE_URL + link

        # # Stop condition
        # if index == 9:
        #     break

        # Get the product data
        product_data = sf.extract_product_data(driver, full_link, new_index)

        # Save the product data
        product_df.loc[index] = product_data
        product_df.to_csv(ppaths.PRODUCT_CSV_PATH, index=False)

##################################################################



####################### CLOSE DRIVER #############################
print("Closing driver...")
driver.quit()
##################################################################
