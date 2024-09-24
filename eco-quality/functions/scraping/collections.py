from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

import parameters.times as pt
import parameters.paths as pp
import functions.scraping.utils as ut

from functions.scraping.utils import write_html_to_file

import time
from random import randint
import re

from bs4 import BeautifulSoup
import pandas as pd

# Function to create filenam from title
def create_filename(name):
    # Remove non-alphanumeric characters and replace spaces with underscores
    filename = re.sub(r'[^a-zA-Z0-9\s]', '', name).strip().replace(' ', '_')
    return filename

# Function to get the main-nav ul
def get_main_nav_ul(driver, url):
    try:
        driver.get(url)
        main_ul = WebDriverWait(driver, pt.MAIN_UL_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'main-nav')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        main_ul = soup.find('ul', class_='main-nav')
        return main_ul

    except TimeoutException:
        print(f"TimeoutException: Main UL not found")

# Function to get the li elements in the dropdown menus
def get_li_elements(dropdown_menus):
    all_li = []
    for dropdown_menu in dropdown_menus:
        all_li.extend(dropdown_menu.find_all('li', class_='', recursive=False))
    return all_li

# Function to get name and link from the li elements
def get_name_and_link(li_elements):
    elements = []
    for li in li_elements:
        a_tag = li.find('a')
        name = a_tag.text.strip()
        link = pp.BASE_URL + a_tag['href']
        elements.append({'url': link, 'name': name, 'filename': create_filename(name)})
    return elements

def get_categories(dropdowns):
    category_dict = {}
    for dropdown in dropdowns:
        dropdown_class = dropdown['class']
        if dropdown_class != "dropdown dropdown-submenu":

            # TODO: create a function for this
            dropdown_inner = dropdown.find('div', class_='dropdown-inner')
            dropdown_link = dropdown_inner.find('a', class_='dropdown-link')
            category_name = dropdown_link.text.strip()
            category_dict[category_name] = []

            # Get the dropdown-menus
            dropdown_menu = dropdown.find('ul', class_='dropdown-menu')
            if dropdown_menu:
                dropdown_lis = dropdown_menu.find_all('li', recursive=False)
                for li in dropdown_lis:
                    if li.has_attr('class'):
                        li_class = li['class']
                        if "dropdown-submenu" in li_class:
                            subcategory_div = li.find('div', class_='dropdown-inner')
                            subcategory_name = subcategory_div.find('a', class_='dropdown-link').text.strip()
                            subcategory_ul = li.find('ul', class_='dropdown-menu')
                            subcategory_lis = subcategory_ul.find_all('li', recursive=False)
                            sub_subcategory_list = []
                            for sub_li in subcategory_lis:
                                sub_li_a = sub_li.find('a')
                                if sub_li_a:
                                    sub_li_name = sub_li_a.text.strip()
                                    sub_li_link = pp.BASE_URL + sub_li_a['href']
                                    sub_subcategory_list.append({sub_li_name: sub_li_link})
                            category_dict[category_name].append({subcategory_name: sub_subcategory_list})
                        else:
                            li_a = li.find('a')
                            if li_a:
                                li_name = li_a.text.strip()
                                li_link = pp.BASE_URL + li_a['href']
                                category_dict[category_name].append({li_name: li_link})
                    else:
                        li_a = li.find('a')
                        li_name = li_a.text.strip()
                        li_link = pp.BASE_URL + li_a['href']
                        category_dict[category_name].append({li_name: li_link})


# Function to get the collections
def get_collections(driver, url, work_with_saved_html):
    try:
        # Get the main UL and save it to work on in later
        if not work_with_saved_html:
            main_ul = get_main_nav_ul(driver, url)
            write_html_to_file(main_ul.prettify(), pp.COLLECTION_MAIN_UL_PATH)
        main_ul = BeautifulSoup(open(pp.COLLECTION_MAIN_UL_PATH, 'r', encoding='utf-8'), 'html.parser')

        # 1. Search for the li with class dropdown
        li_dropdowns = main_ul.find_all("li", class_='dropdown')

        # 2. Get the categories and subcategories
        categories = ut.get_all_categories(li_dropdowns)

        # 3. Create the collection
        collection = ut.create_collection(categories)

        return collection

        # # 2. Search for the ul with class dropdown-menu inside the li
        # dropdown_menus = [li.find('ul', class_='dropdown-menu', recursive=False) for li in li_dropdowns]

        # # 3. Search for final li elements
        # li_elements = get_li_elements(dropdown_menus)

        # # 4. Get the collection data
        # collection = get_name_and_link(li_elements)
    except TimeoutException:
        print(f"TimeoutException: Main UL not found")

# Function to get link and name of product
def get_product_name_and_link(product_h5s):
    products_links = []
    for h5 in product_h5s:
        name = h5.text.strip()
        link = pp.BASE_URL + h5.find('a')['href']
        products_links.append({'url': link, 'name': name})
    return products_links

# Function to save the products links
def save_products_links(products_links, filename, new_csv):
    # 1. Create DataFrame
    products_df = pd.DataFrame(products_links, columns=['url', 'name'])

    # 2. Save in existing CSV, if not, create one
    if new_csv:
        products_df.to_csv(f"data/scraped/{filename}_products_links.csv", index=False)
    else:
        try:
            products_df.to_csv(f"data/scraped/{filename}_products_links.csv", mode='a', header=False, index=False)
        except FileNotFoundError:
            products_df.to_csv(f"data/scraped/{filename}_products_links.csv", index=False)

# Function to get and save the collection page HTML
def get_collection_html(driver, filename, url, from_file, count):
    try:
        if from_file:
            soup = BeautifulSoup(open(f"data/html/collection/{filename}_page={count}.html", 'r', encoding='utf-8'), 'html.parser')
        else:
            driver.get(url)
            catalog_div = WebDriverWait(driver, pt.CATALOG_DIV_TIMEOUT).until(EC.visibility_of_element_located((By.CLASS_NAME, 'cata-product')))
            soup = BeautifulSoup(catalog_div.get_attribute('outerHTML'), 'html.parser')
            write_html_to_file(soup.prettify(), f"data/html/collection/{filename}_page={count}.html")
        return soup
    except Exception as e:
        print("Exception while getting collection's HTML")
        print(f"Exception: {e}")
        return None

# Function to check if a collections has next page
def get_next_page(driver):
    try:
        a_next = WebDriverWait(driver, pt.NEXT_PAGE_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'next')))
        a_next_attributes = a_next.get_attribute('class')
        if 'disabled' in a_next_attributes:
            return None
        return a_next.get_attribute('href')
    except TimeoutException:
        print("TimeoutException: Next page not found")
        return None

# Function to find the products names and links
def fetch_product_links(soup, products_links, count, filename):
    try:
        product_item_divs = soup.find_all('div', class_='product-grid-item')
        product_h5s = [div.find('h5', class_='product-name') for div in product_item_divs]
        product_links = get_product_name_and_link(product_h5s)
        new_csv = True if count == 1 else False
        save_products_links(product_links, filename, new_csv)
        products_links.extend(product_links)
        return products_links

    except Exception as e:
        print("Exeption while getting product's links")
        print(f"Exception: {e}")

# Function to get the product links
def get_product_links(driver, collection, all_products_links):
    finished = False
    url = collection['url']
    filename = collection['filename']
    count = 1
    while not finished:
        time.sleep(randint(4, 8))
        print(f"Getting products links from {url} \n")
        soup = get_collection_html(driver, filename, url, False, count)
        if soup:
            all_products_links = fetch_product_links(soup, all_products_links, count, filename)
            next_page = get_next_page(driver)
            if next_page:
                url = next_page
            else:
                finished = True
        else:
            finished = True
        count += 1
    return all_products_links
