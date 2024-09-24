from selenium.webdriver.common.by import By

# Custom find_element function
def my_find_element(driver, condition, element):
  ''' Avoids crushing program if element not found''' 
  try:
    return driver.find_element(condition, element)
  except:
    print(f'Element {element} with condition {condition} not found')
