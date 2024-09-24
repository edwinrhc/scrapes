from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

import parameters as param
import functions as f

def my_finder(driver, by, desc):
    
    try:
        wait = WebDriverWait(driver, param.TIMEOUT)
        element = wait.until(EC.presence_of_element_located((by,desc)))
    except TimeoutException:
        print("element not found")
        element = ''
        
    return element

def get_element_html(driver, by, desc, name='no name'):

    try:
        # wait = WebDriverWait(driver, param.TIMEOUT)
        wait = WebDriverWait(driver, 5)
        element = wait.until(EC.presence_of_element_located((by,desc)))
        element_html = element.get_attribute('innerHTML')
    except TimeoutException:
        element_html=''
        print(f"Failed to get {name} inner HTML")
    except StaleElementReferenceException:
        element_html=''
        print(f"Failed to get {name} inner HTML")

    return element_html 
      
def get_element_text(driver, by, desc, name):

    wait_time = param.TIMEOUT if name == 'title' or name == 'description' else 5
    try:
        # wait = WebDriverWait(driver, param.TIMEOUT)
        wait = WebDriverWait(driver, wait_time)
        element = wait.until(EC.presence_of_element_located((by,desc)))
        element_text = element.text
    except TimeoutException:
        element_text = ''
        print(f"Failed to get {name} text")
    except StaleElementReferenceException:
        element_text = ''
        print(f"Failed to get {name} text")

    return element_text


def get_case_dimensions(driver):
    
    keys = ['L','W','H']
    dimensions = dict.fromkeys(keys, '')
    dim_list = get_element_text(driver, By.CSS_SELECTOR,"div[data-id='case_dimensions_text']", 'case dimensions').replace('x', '').split()
    if dim_list:
        unit = dim_list.pop()
    
        i = 0
        for dim in dim_list:
            dimensions[keys[i]] = f"{dim} {unit}"
            i+=1

    return dimensions

def get_description(driver):
    
    description = get_element_text(driver, By.CSS_SELECTOR, "div[data-id='product_description_text'", 'description')
    try:
        if description == "Product description is not available":
            print(description)
        else:
            try:
                f.my_click(driver, By.CSS_SELECTOR, "button[data-id='ellipsis-read-more-button']")
                f.my_click(driver, By.CSS_SELECTOR, "button[data-id='ellipsis-read-more-button-on-cooking']")
            except:
                print("Description's 'Read More' button not found")

            description = get_element_text(driver, By.CSS_SELECTOR,"div[class='description-detail-wrapper']", 'description')
            description = description.replace("Read Less", '').strip()
    except:
        print('Could find description text element')
        
    return description

def get_price(driver):
    
    try:
        price = get_element_text(driver, By.CSS_SELECTOR,"div[data-id='display-price']", 'price')
        return price.replace('$', '').split()[0]
    except:
        return ''

def get_stock(driver):
    stock = get_element_html(driver,By.CSS_SELECTOR, "label[data-id='product_details_stock_status_label']", 'stock')
    if stock.replace('"','') == "Out of stock":
        return False
    else:
        return True

def set_category(driver, product_dict):
    
    breadcrumb = my_finder(driver, By.CSS_SELECTOR, "div[class='breadcrumb']")
    cat_levels = len(breadcrumb.find_elements(By.CSS_SELECTOR, "div[class='container']")) if breadcrumb else 0
    # my_finder(driver, By.CSS_SELECTOR, "div[class='crumb-separator']")
    # cat_levels = len(driver.find_elements(By.CSS_SELECTOR, "div[class='crumb-separator']"))
    for i in range(cat_levels):
        # Vendor category start at level 1 (i+1)
        product_dict[f'vendorCategory.{i}'] = get_element_text(driver,By.CSS_SELECTOR, f"button[data-id='breadcrumb_category_level{i+1}']", f"category.{i}")
    
def set_images(driver, product_dict):
    
    main_img_div = my_finder(driver, By.CLASS_NAME, "main-product-image-container-v2")
    try:
        main_img = main_img_div.find_element(By.TAG_NAME, "img").get_attribute('src')
        product_dict['images.0'] = main_img
    except:
        print('No main image')
        return
    
    try:  
        imgs_element = my_finder(driver, By.CLASS_NAME, "slider-image-wrapper-v2")
        if imgs_element:
            imgs_tag = imgs_element.find_elements(By.TAG_NAME, "img")
            imgs = [img.get_attribute('src') for img in imgs_tag]
            # Start from 1 because first img is equal to main one
            for i in range(1,len(imgs)):
                product_dict[f"images.{i}"] = imgs[i]
    
    except:
        print('Only main image available')

def set_specs(driver, product_dict):
    specs = []
    try:
        specs_rows = driver.find_elements(By.CSS_SELECTOR, "div[class='product-spec-description']")
        for spec in specs_rows:
            header = get_element_text(spec, By.CSS_SELECTOR,"div[class='product-spec-header']", 'spec header')
            details = spec.find_elements(By.CSS_SELECTOR, "div[class='product-spec-details']")
            detail = [txt.text for txt in details]
            specs.append((header, '\n'.join(detail)))
            
        # spec_headers = [header.text for header in driver.find_elements(By.CSS_SELECTOR, "div[class='product-spec-header']")]
        # spec_texts = [txt.text for txt in driver.find_elements(By.CSS_SELECTOR, "div[class='product-spec-details']")]
        # specs = list(zip(spec_headers, spec_texts))
        for i in range(len(specs)):
            product_dict[f'specs.{i}.name'] = specs[i][0]
            product_dict[f'specs.{i}.value'] = specs[i][1]
    except:
        print("Failed to find Specs")        
       
def get_product_info(driver, product_url):
    ''' Gathers all fields from the product & returns a dictionary with the info '''
    product_dict = {}
    
    # Fields - Must
    product_dict['url'] = product_url
    product_dict['title'] = get_element_text(driver,By.CSS_SELECTOR, "div[data-id='product_name']", "title")
    product_dict['description'] = get_description(driver)
    product_dict['metaTitle'] = product_dict['title']
    product_dict['metaDescription'] = product_dict['description']
    product_dict['vendor'] = "Sysco"
    product_dict['price'] = get_price(driver)
    set_category(driver, product_dict)
    set_images(driver,product_dict)
    product_dict['upc'] = get_element_text(driver, By.CSS_SELECTOR,"div[data-id='manufacturer_upc_text']", 'upc')
    set_specs(driver, product_dict)
    product_dict['ourCost'] = product_dict['price']

    # Fields - Important (1)
    product_dict['availableForSale'] = get_stock(driver)
    product_dict['brand'] = get_element_html(driver,By.CSS_SELECTOR, "button[data-id='product_brand_link']", "brand")
    product_dict['manufacturerNumber'] = get_element_text(driver, By.CSS_SELECTOR,"div[data-id='gtin_text']", 'gtin') # Listed as GTIN
    product_dict['productMinOrderCases'] = '1'
    product_dict['productMinOrderPrice'] = product_dict['price']
    dimensions_dict = get_case_dimensions(driver)
    product_dict['packageLength'] = dimensions_dict['L']
    product_dict['packageWidth'] = dimensions_dict['W']
    product_dict['packageHeight'] = dimensions_dict['H']
    
    # Fields - Nice to Have (2)

    # Fields - Only if available (3)
    if product_dict['availableForSale']:
        product_dict['shippingFrom'] = get_element_text(driver, By.CSS_SELECTOR,"span[class='availability-opco-text']", 'shippingFrom')

    # Extras for post scrape processing
    product_dict['syscoPackSize'] = get_element_text(driver, By.CSS_SELECTOR,"div[data-id='pack_size']", 'syscoPackSize')
    product_dict['syscoId'] = get_element_text(driver, By.CSS_SELECTOR,"div[data-id='product_id']", 'syscoID')
    
    return product_dict