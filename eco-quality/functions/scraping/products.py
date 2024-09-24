"""Import all neccesary modules"""
import json

from bs4 import BeautifulSoup

import functions.scraping.utils as ut

def get_product_data(driver, soup, collection, variant):
    """Function to get the product data"""

    # Initialize the product attributes
    product = ut.init_product_attributes({})

    # Extract title, description, images
    product['title'] = ut.extract_title(soup)
    product['metaTitle'] = product['title']
    product['description'] = ut.extract_description(soup)
    product['metaDescription'] = product['description']
    ut.extract_images(soup, product)

    # Extract the options. Ex: size, tea_bags, pcs, etc
    ut.extract_options(soup, product)

    # Extract data from meta
    product['vendor'] = ut.extract_vendor(soup)

    # Extract data from variant
    product['URL'] = ut.extract_url(soup) + f"?variant={variant['id']}"
    product['selectedOptions'] = ut.extract_selected_options(soup, variant['id'])
    if len(variant.keys()) > 1:
        product['price'] = variant['full_price']
        product['availableForSale'] = variant['available']
    else:
        driver.get(product['URL'])
        ut.webdriver_wait_page(driver, 10)
        ut.wait_random_time()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product['price'] = ut.extract_price(soup)
        product['availableForSale'] = ut.extract_stock(soup)

    # Extract sku, is available, min order
    product['sku'] = ut.extract_sku(soup)
    product['productMinOrderCases'] = ut.extract_min_order(soup)

    # Extract the vendor categories
    ut.extract_vendor_categories(collection, product)

    return product

def get_product_variants(driver, url, collection, read_from_html):
    """Function to get the product variants"""

    # Get and save the product's HTML
    if not read_from_html:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ut.write_html_to_file(soup.prettify(), f"data/html/products/product_{0}_{0}.html")
    soup = BeautifulSoup(open(f"data/html/products/product_{0}_{0}.html", 'r', encoding='utf-8'), 'html.parser')

    # Wait random time to avoid being blocked
    ut.wait_random_time()

    # Get all the variants
    variants = []
    shopify_terms = soup.find('shopify-payment-terms')
    if shopify_terms:
        shopify_meta = json.loads(shopify_terms['shopify-meta'])
        variants = shopify_meta['variants']
    else:
        product_select = soup.find('select', attrs={'name': 'id'})
        if product_select:
            options = product_select.find_all('option')
            variants = [{"id": option['value']} for option in options]

    # Iterate over the variants and extract the data
    products_list = []
    for variant in variants:
        product = get_product_data(driver, soup, collection, variant)
        products_list.append(product)

    return products_list
