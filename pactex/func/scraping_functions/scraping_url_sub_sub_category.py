from pactex.common import (re,pd, TimeoutException, NoSuchElementException, By, WebDriverWait, EC, params, json)
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, RequestException



def get_url_sub_sub_collection():
    # url = "https://www.pactex.com/bed-bath-linens/shower-curtains.html"
    url = "https://www.pactex.com/bed-bath-linens/towels.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        url_collection_item = soup.select("li.apptrian-subcategories-category-wrapper")
        collection = []

        for item in url_collection_item:
            a_tag = item.find('a', class_='apptrian-subcategories-category')
            if a_tag:
                href = a_tag['href']
                span_tag = a_tag.find('span')
                if span_tag:
                    link_text = span_tag.get_text(strip=True)
                    collection.append({
                        'url_collection': href,
                        'name_collection': link_text
                    })
        print("Las colecciones -> ", collection)
        return collection
    except requests.exceptions.RequestException as e:
        print(f"Error HTTP: {e}")
        return None

