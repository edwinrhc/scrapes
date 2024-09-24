from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from random import randint

import time

import params as params
from functions.scraping_functions.utils import my_find_element

# Function to set the product attributes
def init_product_attributes(product):
  for header in params.HEADERS:
    product[header] = ''
  return product

# Function to check if product is available for sale
def is_product_available(driver):
  add_to_cart_span = my_find_element(driver, By.ID, 'AddToCartText-product-template')
  add_to_cart_text = add_to_cart_span.text.lower()
  if add_to_cart_text == "sold out":
    return False
  return True

# Function to get the product title as it appears in the page
def get_product_title(driver):
  product_title_h1 = my_find_element(driver, By.CLASS_NAME, 'product-single__title')
  product_title_text = product_title_h1.text
  return product_title_text

# Function to get the product title without specs
def get_product_title_without_specs(driver):
  meta_title = my_find_element(driver, By.XPATH, "//meta[@property='og:title']").get_attribute('content')
  return meta_title

# Function to get the <li> > <span> descriptions
def get_product_li_descriptions(driver, by, value):
  elements = driver.find_elements(by, value)
  description = ''
  for item in elements:
    description += item.text + ' '
  return description

# Function to get the text from <p>|<span>
def get_text_from_p_span(elements):
  description = ''
  for element in elements:
    a_links = element.find_elements(By.TAG_NAME, 'a')
    if a_links:
      continue
    else:
      description += element.text + ' '
  return description

# Function to check if list has li elements
def has_li_elements(driver):
  li_elements = driver.find_elements(By.TAG_NAME, 'li')
  if li_elements:
    return True
  return False

# Function to get the product description
def get_product_full_description(driver):
  description_div = my_find_element(driver, By.CLASS_NAME, 'product-single__description')
  description = description_div.text
  return description.strip()

# Function to get product metaDescription
def get_product_meta_description(driver):
  meta_description = my_find_element(driver, By.XPATH, "//meta[@property='og:description']").get_attribute('content')
  return meta_description

# Function to get the product sku
def get_product_sku(driver):
  sku_option = my_find_element(driver, By.XPATH, "//option[@data-sku]")
  sku = sku_option.get_attribute('data-sku')
  return sku

# Function to get the product data
def get_product_data(driver, url, collection):
  # Initialize the product attributes
  product = init_product_attributes({})
  driver.get(url)

  # Wait random time to avoid being blocked
  random_time = randint(params.MIN_PRODUCT_SLEEP, params.MAX_PRODUCT_SLEEP)
  print(f'Waiting {random_time} seconds before scraping the next product...')
  time.sleep(random_time)

  # Get the static data
  product['URL'] = url

  # Get is available for sale
  product['availableForSale'] = is_product_available(driver)

  # Get the product title and meta title
  product['metaTitle'] = get_product_title_without_specs(driver)
  product['title'] = get_product_title(driver)

  # Get product description and meta description
  product['description'] = get_product_full_description(driver)
  product['metaDescription'] = product['description']

  # Get vendor, manufacturer and brand name
  product['vendor'] = my_find_element(driver, By.XPATH, "//meta[@property='og:site_name']").get_attribute('content')
  product['manufacturerName'] = product['vendor']
  product['brand'] = product['vendor']

  # Get model
  product['model'] = 'Undefined for now'

  # Get the price
  product['price'] = my_find_element(driver, By.XPATH, "//meta[@property='og:price:amount']").get_attribute('content')

  # Get the categories
  product['vendorCategory.0'] = collection

  # Get the images
  images = driver.find_elements(By.XPATH, "//meta[@property='og:image:secure_url']")
  for i in range(3):
    if i < len(images):
      product[f'images.{i}'] = images[i].get_attribute('content')

  # Get product UPC & SKU
#   product['upc'] = driver.find_element(By.NAME, 'product-id').get_attribute('value')
#   product['manufacturerNumber'] = product['upc']
  product['sku'] = driver.find_element(By.XPATH, "//option[@data-sku]").get_attribute('data-sku')

  # Get the minimum OrderCases and OrderPrice
  product['productMinOrderCases'] = '1'
  product['productMinOrderPrice'] = product['price']

  # Get the rest of the data
  product['freeShipping'] = 35
  product['canCustomize'] = False
  product['ourCost'] = product['price']
  return product
