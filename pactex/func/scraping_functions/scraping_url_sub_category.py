from pactex.common import (re,pd, TimeoutException, NoSuchElementException, By, WebDriverWait, EC, params, json)
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, RequestException

# def get_url_sub_category(url_Category, category, parent_text):
#     try:
#         response = requests.get(url_Category)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')
#         sub_category_items = soup.select("li.item.product.product-item")
#         products = []
#         for item in sub_category_items:
#             product_name_tag = item.select_one("strong.product.name.product-item-name a")
#             if product_name_tag:
#                 product_name = product_name_tag.text.strip()
#                 product_url = product_name_tag['href']
#                 products.append({
#                     'product_url': product_url,
#                     'product_name': product_name,
#                     'category': category,  # Nombre de la categoría proveniente del CSV
#                     'parent_text': parent_text  # Texto del parent proveniente del CSV
#                 })
#         return products
#     except requests.exceptions.HTTPError as e:
#         print(f"Error HTTP: {e}")
#         return None
#     except requests.exceptions.RequestException as e:
#         print(f"Error en la solicitud: {e}")
#         return None

def get_url_sub_category(url,text):
    # url = "https://www.pactex.com/bed-bath-linens.html"
    # text ="BED & BATH LINEN"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ajusta el selector CSS según la estructura de tu HTML
        sub_category_items = soup.select("ul.apptrian-subcategories-grid li.apptrian-subcategories-category-wrapper")
        products = []

        for item in sub_category_items:
            a_tag = item.find('a', class_='apptrian-subcategories-category')
            if a_tag:
                href = a_tag['href']
                span_tag = a_tag.find('div', class_='apptrian-subcategories-category-name').find('span')
                if span_tag:
                    sub_category_name = span_tag.get_text(strip=True)
                    products.append({
                         'sub_category_url': href,
                         'sub_category_name': sub_category_name,
                         'category_url': url,
                         'category': text
                         })

        return products

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None

