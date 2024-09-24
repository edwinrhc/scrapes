from dzeeusa.common import (re, requests,pd, TimeoutException, NoSuchElementException, By, WebDriverWait, EC, params, json)

from bs4 import BeautifulSoup


def get_url_list_products(driver, product_url):
    """Extrae detalles de todos los productos desde la página."""
    driver.get(product_url)
    try:
        product_elements = WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, "li.item.product-item div.listpro-right a.product-item-link")))

        product_details = []
        for element in product_elements:
            product_url = element.get_attribute("href")
            product_details.append({'url_products': product_url})

        return product_details
    except NoSuchElementException as e:
        print(f"No se pudo encontrar el elemento: {e}")
        return None
    except TimeoutException as e:
        print(f"Tiempo de espera excedido: {e}")
        return None

