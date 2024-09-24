from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

import parameters as param

def my_click(driver, by, desc):
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((by, desc))).click()
    
def change_language(driver, language="English"):
    
    try:
        actual_language = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='language-text']")))
        if actual_language.text != language:
            actual_language.click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li[text()={language}]"))).click()
        print(f"Succesfully changed language to {language}")
        changed_language = True
        
    except:
        print(f'Failed changing language to {language}')
        changed_language = False
        
    return changed_language

def get_products_urls(driver):
    ''' Get url of all products present in current page (max = 24)
        return list with all url'''
    urls = []
    try:
        products_wraper = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"catalog-cards-wrapper")))
        products = products_wraper.find_elements(By.CLASS_NAME, 'product-card-link')
        for product in products:
            urls.append(product.get_attribute('href'))
    except:
        print("Product urls not found")

    return urls

def guest_login(driver, zip_code):
    
    my_click(driver, By.CSS_SELECTOR, "button[data-id='btn_login_continue_as_guest'")
    zip_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[data-id='initial_zipcode_modal_input']")))
    zip_input.send_keys(zip_code)
    zip_input.send_keys(Keys.ENTER)

def next_page_by_btn(driver):
    ''' Go to next page '''

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-id='button_page_next'"))).click()
    except:
        print("no next page")
           
def next_page_by_url(url):
    ''' Looks for "page=" in url and return next or add and returns same url with "page=xx+1" '''
    if "page=" in url:
        for i in url.split("&"):
            if "page" in i:
                current_page = i
                next_page_num = str(int(i.split("=")[-1])+1)
        next_page_url = url.replace(current_page, f"page={next_page_num}")
        return next_page_url

    # First page has different format
    else:
        return url.replace("&ITEM_GROUP_ID", "&typeAhead=false&ITEM_GROUP_ID") + "&page=2"

def products_to_csv(products_dict, filename):
    product_counter = 0
    with open(filename, 'w', newline='', encoding='utf-8') as file_: 
        writer = csv.DictWriter(file_, fieldnames=param.HEADERS)
        writer.writeheader()
        
        for product in products_dict:
            writer.writerow(product)
            product_counter +=1
    
    print(f'Succesfuly saved {product_counter} products to {filename}.csv')
    
def user_login(driver, username, password):
    
    try:
        user_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[data-id='txt_login_email']")))
        user_input.send_keys(username)
        pass_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"okta-signin-password")))
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        
        logged_in = True
        print("Succesfully logged in")
    except:
        logged_in = False
    
    return logged_in




