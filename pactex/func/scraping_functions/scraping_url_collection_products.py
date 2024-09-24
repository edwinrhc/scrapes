from pactex.common import (re,pd, TimeoutException, NoSuchElementException, By, WebDriverWait, EC, params, json)
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, RequestException



def get_url_collection():
    url = "https://www.pactex.com/housekeeping-janitorial/cleaners.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        url_collection_item = soup.select("li.item.product.product-item")
        collection= []

        for item in url_collection_item:
            a_tag = item.find('a',class_='product-item-link')
            button_tag = item.find('button', class_='action tocart primary grp_view_items_btn')
            if a_tag and button_tag:
                href = a_tag['href']
                link_text = a_tag.get_text(strip=True)
                button_text = button_tag.get_text(strip=True)
                collection.append({
                    'url_collection': href,
                    'name_collection':link_text,
                    'button_text': button_text
                })
        print("Las colecciones -> ", collection)
        return collection
    except requests.exceptions.RequestException as e:
        print(f"Error HTTP: {e}")
        return None
