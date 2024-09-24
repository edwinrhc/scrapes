from dzeeusa.common import (re, requests,pd, TimeoutException, NoSuchElementException, By, WebDriverWait, EC, params, json)

from bs4 import BeautifulSoup

def get_url_list_products(product_url, sub_category,category):
    """Extrae detalles de todos los productos desde la página utilizando requests y BeautifulSoup."""
    sub_category = sub_category
    category = category
    try:
        response = requests.get(product_url)
        response.raise_for_status()  # Asegura que la solicitud fue exitosa
        soup = BeautifulSoup(response.text, 'html.parser')

        # Asumiendo que el selector para los productos es correcto
        product_elements = soup.select("li.item.product-item div.listpro-right a.product-item-link")

        # Utilizar un conjunto para almacenar URLs y asegurar que no haya duplicados
        seen_urls = set()
        product_details = []
        for element in product_elements:
            product_url = element['href']  # Extrae el href directamente del atributo
            # Verificar si la URL ya ha sido procesada
            if product_url not in seen_urls:
                seen_urls.add(product_url)
                product_details.append({'url_products': product_url,'category':category ,'sub_category': sub_category})

        #print(product_details)
        return product_details

    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None
