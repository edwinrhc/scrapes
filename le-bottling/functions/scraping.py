"""Import necessary liobraries"""
import csv
import time


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
from random import randint

import parameters.paths as ppaths
import functions.scraping_utils as fsu

def get_login(driver):
    """Function to get the login page"""
    try:
        driver.get(ppaths.LOGIN_URL)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'workArea')))
        return True
    except TimeoutException:
        print("TimeoutException: Fail to load LOGIN PAGE, the page took too long to load")
        return False

def user_login(driver, username, password):
    """Function to login to the website"""
    try:
        # First set the username
        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'emailInput')))
        username_input.send_keys(username)
        username_input.send_keys(Keys.ENTER)

        # Then set the password
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordInput')))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        return True
    except TimeoutException:
        print("TimeoutException: Fail to LOGIN, the page took too long to load")
        return False

def get_products_page(driver):
    """Function to wait for the main page to load"""

    # Get soup and save html
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    with open(ppaths.LANDING_HTML_PATH, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    # Get the link
    links_div = soup.find('div', class_='list-group visible-lg main-actions')
    a_tag = links_div.find('a', attrs={'ui-sref': 'search'})
    href = a_tag['href']

    # Go to the products page
    full_url = ppaths.LANDING_BASE_URL + href
    print(f"Full URL: {full_url}")
    driver.get(full_url)

    # Wait for the products page to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ng-star-inserted')))
        print("Products page loaded")
    except TimeoutException:
        print("TimeoutException: Fail to load PRODUCTS PAGE, the page took too long to load")
        return False
    return True

def get_products_links(soup):
    """Function to get all the links of the products"""
    try:
        items_bodys = soup.find_all('div', class_='item-body')
        items_titles = [item.find('div', class_='mat-title') for item in items_bodys] if items_bodys else []
        items_links = [item.find('a')['href'] for item in items_titles] if items_titles else []
        return items_links
    except NoSuchElementException:
        print("NoSuchElementException: Fail to get products links, the element does not exist")
        return []

def get_next_page(driver, soup):
    """Function to get the next page"""
    try:
        next_button = soup.find('button', class_='mat-paginator-navigation-next')
        is_disabled = next_button.has_attr('disabled')
        if not is_disabled:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'mat-paginator-navigation-next')]")))
            next_button.click()
            return True
        return False
    except NoSuchElementException:
        print("NoSuchElementException: Fail to get next page, the element does not exist")
        return False

def save_list_in_csv(path, data, headers):
    """Function to save the data in csv"""
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if headers != []:
            writer.writerow(headers)

        for row in data:
            writer.writerow([row])

def get_all_products_links(driver):
    """Function to get all products links"""
    links_extracted = False
    links = []
    while not links_extracted:
        try:
            # Wait time
            wait_time = randint(5, 10)
            print(f"Wating {wait_time} seconds")
            time.sleep(wait_time)

            # Get the links
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            urls = get_products_links(soup)

            # Print the links
            print("Sacraped the following urls:")
            print(urls)
            print("\n")

            # Save the links
            links.append(urls)
            save_list_in_csv(ppaths.PRODUCTS_LINKS_PATH, links, [])

            # Get the next page
            next_page = get_next_page(driver, soup)
            if not next_page:
                links_extracted = True
                break

        except TimeoutException:
            print("TimeoutException: Fail to get all products links, the page took too long to load")
            return []

    return links

def get_products_links_from_csv():
    """Function to get the products links from csv"""
    with open(ppaths.PRODUCTS_LINKS_PATH, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        links = []
        for row in reader:
            for link in row:
                links.append(link)
        return links

def save_html(soup, index):
    """Function to save the html"""
    with open(f"data/html/products/product_{index}.html", 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

def load_product_page(driver, link):
    """Function to load the product page"""
    max_num_tries = 2
    num_tries = 0
    driver.get(link)
    while num_tries < max_num_tries:
        print(f"Trying to load product page: {link} - Attempt {num_tries + 1}")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'item-layout')))
            break
        except TimeoutException:
            print("TimeoutException: Fail to load product page, the page took too long to load")
            num_tries += 1

def open_nutrition_facts(driver, url):
    """Function to open the nutrition facts"""
    print("Opening nutrition facts")
    try:
        link_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'nutrition-fact-link')))
        link = link_div.find_element(By.TAG_NAME, 'a')
        link.click()
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'cdk-overlay-pane')))
    except TimeoutException:
        print("TimeoutException: Fail to open nutrition facts, the page took too long to load")
        fsu.save_url_in_csv(url)

    except ElementClickInterceptedException:
        print("ElementClickInterceptedException: Fail to open nutrition facts, the element is not clickable")
        fsu.save_url_in_csv(url)


def extract_product_data(driver, url, index):
    """Function to extract the product data"""

    # Get the product page
    load_product_page(driver, url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Wait time to avoid being blocked
    wait_time = randint(5, 10)
    print(f"Waiting {wait_time} seconds...")
    time.sleep(wait_time)

    print(f"Extracting data from product: {index}")

    # Initialize the product dict
    product = {}

    # Get product url
    product['url'] = url

    # Get the product title
    product['title'] = fsu.extract_title(soup)

    # Get the product description
    product['description'] = fsu.extract_description(soup)

    # Get brand, type and id
    sub_descriptions = fsu.extract_sub_descriptions(soup)
    product['brand'] = sub_descriptions[0]
    product['type'] = sub_descriptions[1]
    product['id'] = sub_descriptions[2]

    # Get price and stock
    price_stock = fsu.extract_price_stock(soup)
    product['stock'] = price_stock[0]
    product['price'] = price_stock[1]

    # Extract UPC codes
    upcs = fsu.extract_upcs(soup)
    product['box_upc'] = upcs[0]
    product['retail_upc'] = upcs[1]
    product['unit_upc'] = upcs[2]

    # Extract images
    images = fsu.extract_images(soup)
    product['images'] = images

    # Extract product values
    product['product_values'] = fsu.extract_product_value(soup)

    # Open Nutrition Facts
    open_nutrition_facts(driver, url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    save_html(soup, index)

    # Extract volume and ingredients
    product['volume'] = fsu.extract_volume(soup)
    product['ingredients'] = fsu.extract_ingredients(soup)

    print(f"Product volume: {product['volume']}")
    print(f"Product ingredients: {product['ingredients']}")

    return product

def extract_product_data_soup(soup):
    """Function to extract the product data"""

    # Check for spinner
    spinner = soup.find('mat-spinner', class_='mat-spinner')
    if spinner:
        print("SPINNER FOUND")

    # Initialize the product dict
    product = {}

    # Get the product title
    product['title'] = fsu.extract_title(soup)

    # Get the product description
    product['description'] = fsu.extract_description(soup)

    # Get brand, type and id
    sub_descriptions = fsu.extract_sub_descriptions(soup)
    product['brand'] = sub_descriptions[0]
    product['type'] = sub_descriptions[1]
    product['id'] = sub_descriptions[2]

    # Get price and stock
    price_stock = fsu.extract_price_stock(soup)
    product['stock'] = price_stock[0]
    product['price'] = price_stock[1]

    # Extract UPC codes
    upcs = fsu.extract_upcs(soup)
    product['box_upc'] = upcs[0]
    product['retail_upc'] = upcs[1]
    product['unit_upc'] = upcs[2]

    # Extract images
    images = fsu.extract_images(soup)
    product['images'] = images

    # Extract volume
    product['volume'] = fsu.extract_volume(soup)

    # Extract ingredients
    product['ingredients'] = fsu.extract_ingredients(soup)

    # Extract product values
    product['product_values'] = fsu.extract_product_value(soup)

    return product

def print_product(product_dict):
    """Function to print the product data"""
    for key in product_dict:
        print(f"{key}: {product_dict[key]}")
    print("\n")
