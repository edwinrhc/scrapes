from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from functions.scraping_functions.utils import my_find_element

from random import randint

import params as params

# Function to get the products links from a collection
def get_products_links(driver, url, by, value):
  try:
    driver.get(url)
    elements = WebDriverWait(driver, params.TIMEOUT).until(EC.visibility_of_all_elements_located((by, value)))
    products_links = [element.get_attribute('href') for element in elements]
    return products_links
  except TimeoutException:
    raise RuntimeError('TimeoutException: Exceeded the timeout of webpage')
  
# Function to check if a collections has next page
def get_next_page(driver, by, value):
  try:
    span_next = driver.find_element(by, value)
    next_page = span_next.find_element(By.TAG_NAME, 'a').get_attribute('href')
    return next_page
  except NoSuchElementException:
    return None
  
# Function to get collection path and name
def get_name_and_link(elements):
  collections = []
  for element in elements:
    element_link = element.find_element(By.TAG_NAME, 'a')
    if element_link:
      collection = {
        'name': element_link.text,
        'url': element_link.get_attribute('href')
      }
      collections.append(collection) 
  return collections

# Function to get the collection paths
def get_collections_data(driver, url):
  try:
    driver.get(url)
    nav_button = WebDriverWait(driver, params.TIMEOUT).until(EC.visibility_of_element_located((By.ID, 'SiteNavLabel-shop-catalog')))
    nav_button.click()
    nav_links_div = WebDriverWait(driver, params.TIMEOUT).until(EC.visibility_of_element_located((By.ID, 'SiteNavLinklist-shop-catalog')))
    li_elements = nav_links_div.find_elements(By.TAG_NAME, 'li')
    collections = get_name_and_link(li_elements)
    return collections
  except TimeoutException:
    raise RuntimeError('TimeoutException: Exceeded the timeout of webpage')

# Function to loop trought the collections pages
def loop_collections_pages(driver, url, by, value):
  products_links = []
  products_retrieved = False
  while not products_retrieved:
    products_url = get_products_links(driver, url, by, value)
    products_links += products_url
    next_page = get_next_page(driver, By.CLASS_NAME, 'next')
    if next_page:
      url = next_page
    else:
      products_retrieved = True
  return products_links