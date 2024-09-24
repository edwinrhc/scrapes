"""Import the necessary libraries"""
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
from bs4 import BeautifulSoup

import functions.scraping.utils as ut

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


################### SET IMAGES TO MISSING ####################
products_df = pd.read_csv('ecoquality_products_v4.csv', keep_default_na=False, low_memory=False)
products_done = []
products_images = {}
for index, row in products_df.iterrows():

    print(f"Processing {row['title']}...")

    if row['images.0'] == '' and row['title'] not in products_done:

        print(f"Adding missing images to {row['title']}")

        # Get the product's url
        url = row['URL']

        # Get the product's HTML
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'slider-main-image')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Get the images
            row = ut.extract_missing_images(soup, row)

            # Add them to the list
            products_done.append(row['title'])
            products_images[row['title']] = [
                row['images.0'],
                row['images.1'],
                row['images.2'],
                row['images.3'],
                row['images.4'],
                row['images.5'],
            ]

        except Exception as e:
            print(f"Exception: {e}")

    elif row['images.0'] == '' and row['title'] in products_done:
        row['images.0'] = products_images[row['title']][0]
        row['images.1'] = products_images[row['title']][1]
        row['images.2'] = products_images[row['title']][2]
        row['images.3'] = products_images[row['title']][3]
        row['images.4'] = products_images[row['title']][4]
        row['images.5'] = products_images[row['title']][5]

    else:
        # Add them to the list
        if row['title'] not in products_done:
            products_done.append(row['title'])
            products_images[row['title']] = [
                row['images.0'],
                row['images.1'],
                row['images.2'],
                row['images.3'],
                row['images.4'],
                row['images.5'],
                ]

    # Save the row
    products_df.loc[index] = row

    # Save the DataFrame
    products_df.to_csv('ecoquality_products_v5.csv', index=False)

##############################################################

###################### CLOSING DRIVER ########################
print('Closing driver...')
driver.quit()
##############################################################
