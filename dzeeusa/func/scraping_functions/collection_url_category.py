from dzeeusa.common import (re,pd, TimeoutException, NoSuchElementException, By, WebDriverWait, EC, params, json)
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, RequestException

def getUrlsCategory(driver, url):
    driver.get(url)
    try:
        # Esperar a que la página esté completamente cargada
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'body')))

        # Obtener el HTML de la página y pasar a BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        all_urls = []
        for level in range(4):  # Asumiendo que hay hasta 4 niveles (0 a 3)
            elements = soup.select(f'li.ui-menu-item.level{level} > a')
            for element in elements:
                span_element = element.find('span')
                if span_element:
                    text = span_element.text.strip()
                else:
                    text = 'No text available'  # Puedes ajustar este valor según lo que desees en caso de no haber texto.

                parent = element.find_parent('li', class_=f'level{level-1}')
                parent_text = parent.find('a').find('span').text.strip() if parent and parent.find('a') and parent.find('a').find('span') else ''

                url_data = {
                    'url': element['href'],
                    'text': text,
                    'level': f'Nivel {level}',
                    'parent_text': parent_text
                }
                all_urls.append(url_data)
        #print(list(all_urls))

        # Eliminar duplicados basados en URL y devolver
        unique_urls = {item['url']: item for item in all_urls}.values()
        return list(unique_urls)

    except TimeoutException as e:
        print(f"Tiempo de espera excedido: {e}")
        return None


def getUrlHomeTextiles():
    url = "https://dzeeusa.com/home-textiles.html"
    textiles_data = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select("div.column.main div.category-description div.pagebuilder-column a")
        seen_urls = set()

        for link in links:
            productURL = link.get('href')
            productText = link.text.strip()
            if productText and productText != "View Products" and productURL not in seen_urls:
                seen_urls.add(productURL)
                textiles_data.append({'text': productText, 'url': productURL})

    except requests.exceptions.RequestException as e:
        print(f"Error de red o HTTP: {e}")
    return textiles_data