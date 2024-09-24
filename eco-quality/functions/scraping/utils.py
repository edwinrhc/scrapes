"""Import neccesary modules"""
import re
import time

from random import randint

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import parameters.products as ppr
import parameters.paths as pp

############### PRODUCTS UTILS ###############
def webdriver_wait_page(driver, wait_time):
    """Function to wait for the page to load"""
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, '//body')))
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'product-info')))

def wait_random_time():
    """Funtion to wait a random time"""
    random_wait_time = randint(4, 8)
    print(f"Waiting {random_wait_time} seconds before scraping...")
    time.sleep(random_wait_time)

def init_product_attributes(product):
    """Function initialize the product's attributes"""
    for header in ppr.HEADERS:
        product[header] = ''
    return product

def write_html_to_file(html, filename):
    """Function to write HTML to a file"""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html)

def extract_title(soup):
    """Function to extract the product's title"""
    title_container = soup.find('div', class_='product-info-inner')
    title = title_container.find('h1').text.strip()
    return title

def extract_description(soup):
    """Function to extract the product's description"""
    description_container = soup.find('div', id='tabs-description')
    description = description_container.text.strip()
    return description

def extract_images(soup, product_dict):
    """Function to extract the product's images"""

    # Get the images containers
    images_container = soup.find('div', class_='slider-main-image')
    images_track = images_container.find('div', class_='slick-track')
    images_slides = images_track.find_all('div', class_='slick-slide')

    # Iterate over images and extract them
    max_images = 6
    for index, slide in enumerate(images_slides):
        if (index + 1) == max_images:
            break
        # aria_hidden = slide['aria-hidden']
        # if aria_hidden == 'false':
        image_item = slide.find('div', class_='slick-item')
        if image_item is not None:
            image = image_item.find('img')
            image_src = image['src'] if image else ""
            product_dict[f"images.{index}"] = image_src

def extract_images_og(soup, product_dict):
    """Function to extract the images from meta:og"""

    # Get the images from meta:ig
    meta_images = soup.find_all('meta', attrs={'property': 'og:image'})
    if meta_images:
        max_images = 6
        for index, meta_image in enumerate(meta_images):
            if (index + 1) == max_images:
                break
            image_src = meta_image['content']
            product_dict[f"images.{index}"] = image_src

def extract_options(soup, product_dict):
    """Function to extract the different options of the product"""

    # Get the selectors wrappers
    selector_wrappers = soup.find_all('div', class_='selector-wrapper')

    # Iterate over the selectors and extract the options
    if selector_wrappers:
        index = 0
        for selector_wrapper in selector_wrappers:
            selector_label = selector_wrapper.find('label')
            selector_name = selector_label.text.strip() if selector_label else ""
            selector = selector_wrapper.find('select', class_='single-option-selector')
            options = selector.find_all('option')
            values = [opt.text.strip() for opt in options if opt.text.strip()]
            for val in values:
                product_dict[f"option.{index}.name"] = selector_name
                product_dict[f"option.{index}.value"] = val
                index += 1
    else:
        print("No options found")

def extract_selected_options(soup, variant_id):
    """Function to extract the selected options"""

    product_select = soup.find('select', attrs={'name': 'id'})
    if product_select:
        selected_option = product_select.find('option', attrs={'value': variant_id})
        if selected_option:
            return selected_option.text.strip()
    return ""

def extract_price(soup):
    """Function to extract the product price"""
    detail_price = soup.find('div', class_='detail-price')
    price = detail_price.find('span').text.strip()
    if price:
        return price
    return ""

def extract_url(soup):
    """Function to extract the product URL"""
    meta_url = soup.find('meta', attrs={'property': 'og:url'})
    url = meta_url['content']
    if url:
        return url
    return ""

def extract_vendor(soup):
    """Function to extract the product vendor"""
    meta_vendor = soup.find('meta', attrs={'property': 'og:site_name'})
    vendor = meta_vendor['content']
    if vendor:
        return vendor
    return ""

def extract_sku(soup):
    """Function to extract the product SKU"""
    sku_ul = soup.find('ul', class_='product-sku-collection')
    if sku_ul:
        sku_li = sku_ul.find('li', class_='product-code')
        sku = sku_li.find('span', id='sku').text.strip()
        if sku:
            return sku
    return ""

def extract_stock(soup):
    """Function to check is there is stock"""
    stock_container = soup.find('div', id='stock')
    if stock_container:
        stock_span = stock_container.find('span', class_='stock')
        stock = stock_span.text.strip()
        if stock == 'In Stock':
            return True
    return False

def extract_min_order(soup):
    """Function to extract the minimum order"""
    quantity_container = soup.find('div', class_='quantity-product')
    if quantity_container:
        quantity_input = quantity_container.find('input', id='quantity')
        min_order = quantity_input['value'] if quantity_input else 1
        if min_order:
            return min_order
    return ""

def extract_vendor_categories(collection, product_dict):
    """Function to extract the vendor categories"""
    index = 0
    if collection['category'] != '':
        product_dict[f"vendorCategory.{index}"] = collection['category']
        index += 1
    if collection['subcategory'] != '':
        product_dict[f"vendorCategory.{index}"] = collection['subcategory']
        index += 1
    if collection['sub_subcategory'] != '':
        product_dict[f"vendorCategory.{index}"] = collection['sub_subcategory']
        index += 1
    return product_dict

def extract_missing_images(soup, row):
    """Function to extract the product's images"""

    # Get the images containers
    images_container = soup.find('div', class_='slider-main-image')
    images_track = images_container.find('div', class_='slick-track')
    images_slides = images_track.find_all('div', class_='slick-slide')

    # Iterate over images and extract them
    max_images = 6
    for index, slide in enumerate(images_slides):
        if (index + 1) == max_images:
            break
        # aria_hidden = slide['aria-hidden']
        # if aria_hidden == 'false':
        image_item = slide.find('div', class_='slick-item')
        if image_item is not None:
            image = image_item.find('img')
            image_src = image['src'] if image else ""
            row[f"images.{index}"] = image_src

    return row

##############################################

############### COLLECTIONS UTILS ###############
def get_category_name(dropdown):
    """Function to get the category name"""
    dropdown_inner = dropdown.find('div', class_='dropdown-inner')
    dropdown_link = dropdown_inner.find('a', class_='dropdown-link')
    category_name = dropdown_link.text.strip()
    return category_name

def get_dropdown_menu_lis(dropdown):
    """Function to get the li inside the dropdown-menu"""
    dropdown_menu = dropdown.find('ul', class_='dropdown-menu')
    if dropdown_menu is not None:
        dropdown_lis = dropdown_menu.find_all('li', recursive=False)
        return dropdown_lis
    return []

def set_subcategory(li):
    """Function to set the subcategory data"""
    li_a = li.find('a')
    if li_a is not None:
        li_name = li_a.text.strip()
        li_link = pp.BASE_URL + li_a['href']
        return {li_name: li_link}
    return {}

def set_sub_subcategory(subcategory_lis):
    """Function to set the sub-subcategory data"""
    sub_subcategory_list = []
    for sub_li in subcategory_lis:
        sub_li_a = sub_li.find('a')
        if sub_li_a is not None:
            sub_li_name = sub_li_a.text.strip()
            sub_li_link = pp.BASE_URL + sub_li_a['href']
            sub_subcategory_list.append({sub_li_name: sub_li_link})
    return sub_subcategory_list

def get_sub_subcategory(li):
    """Function to get the subcategory lis"""
    subcategory_div = li.find('div', class_='dropdown-inner')
    subcategory_name = subcategory_div.find('a', class_='dropdown-link').text.strip()
    subcategory_ul = li.find('ul', class_='dropdown-menu')
    subcategory_lis = subcategory_ul.find_all('li', recursive=False)
    sub_subcategory_list = set_sub_subcategory(subcategory_lis)
    return {subcategory_name: sub_subcategory_list}

def get_subcategory(li):
    """Function to get the subcategory"""
    subcategory = {}
    if li.has_attr('class'):
        li_class = li['class']
        if "dropdown-submenu" in li_class:
            subcategory = get_sub_subcategory(li)
        else:
            subcategory = set_subcategory(li)
    else:
        subcategory = set_subcategory(li)

    if subcategory is not None:
        return subcategory


def get_all_categories(dropdowns):
    """Function to get all categories"""
    category_dict = {}
    for dropdown in dropdowns:
        dropdown_class = dropdown['class']
        if "dropdown-submenu" not in dropdown_class:

            # 1. Get the category name
            category_name = get_category_name(dropdown)
            category_dict[category_name] = []

            # 2. Get the li inside the dropdown-menu
            dropdown_lis = get_dropdown_menu_lis(dropdown)

            # 3. Get the subcategories
            for li in dropdown_lis:
                subcategory = get_subcategory(li)
                category_dict[category_name].append(subcategory)
    return category_dict

def create_filename(name):
    """"Function to create a filename"""
    # Remove non-alphanumeric characters and replace spaces with underscores
    filename = re.sub(r'[^a-zA-Z0-9\s]', '', name).strip().replace(' ', '_')
    return filename

def create_collection(categories):
    """Function to create the collection"""
    collection = []
    for category in categories:
        category_name = category
        subcategories = categories[category]
        for subcategory in subcategories:
            subcategory_name = list(subcategory.keys())[0]
            if subcategory[subcategory_name].__class__ == list:
                sub_subcategories = subcategory[subcategory_name]
                for sub_subcategory in sub_subcategories:
                    sub_subcategory_name = list(sub_subcategory.keys())[0]
                    sub_subcategory_link = sub_subcategory[sub_subcategory_name]
                    collection.append({'category': category_name, 'subcategory': subcategory_name, 'sub_subcategory': sub_subcategory_name, 'name': sub_subcategory_name, 'filename': create_filename(sub_subcategory_name), 'url': sub_subcategory_link})
            else:
                subcategory_link = subcategory[subcategory_name]
                collection.append({'category': category_name, 'subcategory': subcategory_name, 'sub_subcategory': '', 'name': subcategory_name, 'filename': create_filename(subcategory_name), 'url': subcategory_link})
    return collection
#################################################
