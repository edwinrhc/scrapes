import csv
import os

from random import randint
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

import parameters as param
import functions as f
from product_functions import get_product_info

# Selenium CONFIG
chrome_options = Options()
service = Service(ChromeDriverManager().install())

# Driver SETTINGS
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument('--lang=en_US')
chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--log-level=3') # Minimal logs in console (only fatal errors)

# Driver START
driver = webdriver.Chrome(service=service, options=chrome_options)
url = param.BASE_URL

# Login
driver.get(url)
# f.guest_login(driver, zip_code='77034')

username = os.environ.get("USER_SYSCO")
password = os.environ.get("PASS_SYSCO")
logged_in = f.user_login(driver, username, password)
f.user_login(driver, username, password)

if logged_in:
    overall_time = time()
    sleep(10)

    # Start counters
    product_counter = 0 # number of products
    products_acc_time = 0 # accumulated time on products requests
    product_avg_time = 0 # For monitoring delays (might indicate server suspiciuos)

    # Set category - WORKING BY CATEGORY (Add loop trough categories when using Beautiful Soup)
    category = 'suppliesequipment&ITEM_GROUP_ID=syy_cust_tax_kitchenandcutlery'
    category_name = category.replace("&ITEM_GROUP_ID=syy_cust_tax", '')
    end_category = False

    current_url = param.CATEGORY_BASE_URL + category
    # page_num = '46'
    # current_url = f'https://shop.sysco.com/app/catalog?BUSINESS_CENTER_ID=syy_cust_tax_suppliesequipment&typeAhead=false&ITEM_GROUP_ID=syy_cust_tax_kitchenandcutlery&page={page_num}'
    driver.get(current_url)
    
    
    # Open CSV and define table headers
    with open(f'{category_name}.csv', 'w', newline='', encoding='utf-8') as file_:
        writer = csv.DictWriter(file_, fieldnames=param.HEADERS)
        writer.writeheader()

        while not end_category and logged_in:
            sleep(randint(6,9))
            print(f"Starting with page {current_url[-3:].replace('e','').replace('=','')}")
            products_urls = f.get_products_urls(driver)

            # products_urls = [] # Use for specific products
            if products_urls:
                for product_url in products_urls:
                    print("Starting with next product...")
                    driver.get(product_url)
                    sleep(randint(2,6))
                    product_time = time()
                    product_dict = get_product_info(driver, product_url) # Returns dictionary with product info

                    # Update counters
                    product_counter += 1
                    product_response_time = time() - product_time
                    products_acc_time += product_response_time
                    product_avg_time = products_acc_time/product_counter
                    
                    # Save current product & write to csv
                    writer.writerow(product_dict)

                    
                    print(f'''
                    Total scraped products: {product_counter}
                    Product Time: {product_response_time} s
                    Avg. Product Time: {product_avg_time} s
                    Total time: {products_acc_time} s''')
                    
                    
                    if product_counter == 60:
                        sleep(30)
                        
                current_url = f.next_page_by_url(current_url)
                driver.get(current_url)

            else:
                print(f"Finished scraping {category} category")
                print(f"Total of {product_counter} products scraped")
                end_category = True
                
else:
    print("Failed to log in")

print(f'Overall time elasped: {time() - overall_time}')
driver.quit()
