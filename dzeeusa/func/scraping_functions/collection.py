from dzeeusa.common import (re, requests,pd, TimeoutException, NoSuchElementException, By, WebDriverWait, webdriver_context,EC, params, json)

from bs4 import BeautifulSoup



def extract_volume_pricing(soup):
    volume_prices = []
    volume_price_section = soup.select_one(".tierprice-section")
    if volume_price_section:
        price_rows = volume_price_section.select("tr")
        for row in price_rows:
            cells = row.select("td")
            for cell in cells:
                text = cell.get_text(strip=True)
                if '+' in text:  # Identificamos filas
                    quantity = text.split('+')[0].strip()
                    price_text = cell.find('span', class_="font-bold").get_text(strip=True)
                    # Separar el precio de la unidad
                    price_value = re.sub(r'[^\d.]', '', price_text)  # Extrae solo los dígitos y el punto decimal
                    price_unit = re.sub(r'[\d.$/]', '', price_text).strip()  # Elimina dígitos, dólar, punto y slash
                    volume_prices.append({'quantity': quantity, 'price': price_value, 'unit': price_unit})
                   # print(volume_prices)
    return volume_prices

def get_details_products(driver, product_detail_url):
    "Configuracion"
    try:
        driver.get(product_detail_url)
    except Exception as e:
        print(f"Error al acceder a la URL con Selenium: {e}")
        return None
    try:
        response = requests.get(product_detail_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL con requests: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    product_details = {}

    try:
        ##########################################################
        "Vendor"
        try:
            title_vendor_elements = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.header.content a.logo"))
            )
            if title_vendor_elements:
                product_details['vendor'] = title_vendor_elements[0].get_attribute('title')
        except (NoSuchElementException, TimeoutException) as e:
            print(f"No se puedo encontrar el elemento: 'vendor' :{e}")
            product_details['vendor'] = None

        ##########################################################
        "Title"
        try:
            product_title_elements = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.column.main h1.page-title span.base"))
            )
            if product_title_elements:
                product_details['title'] = product_title_elements[0].text.strip()
                product_details['metaTitle'] = product_title_elements[0].text.strip()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"No se puedo encontrar el elemento: 'title' :{e}")
            print(f"No se puedo encontrar el elemento: 'metaTitle' :{e}")
            product_details['title'] = None
            product_details['metaTitle'] = None

        ##########################################################
        "Price"
        try:
            product_price_elements = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.column.main div.product-info-main div.product-info-price span.price-wrapper"))
            )
            if product_price_elements:
                product_details['price'] = product_price_elements[0].get_attribute('data-price-amount')
        except (NoSuchElementException, TimeoutException) as e:
            print(f"No se puedo encontrar el elemento: 'price' :{e}")
            product_details['price'] = None

        ##########################################################
        "Products description metaDescription"
        try:
            product_details_elements = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.product.attribute.description li"))
            )
            li_descriptions = []
            for li in product_details_elements:
                li_descriptions.append(li.text.strip())
            product_details['description'] = li_descriptions
            product_details['metaDescription'] = li_descriptions
        except (NoSuchElementException, TimeoutException) as e:
            print(f"No se puedo encontrar el elemento: 'description' :{e}")
            print(f"No se puedo encontrar el elemento: 'metaDescription' :{e}")
            product_details['description'] = None
            product_details['metaDescription'] = None

        ##########################################################
        "State - True False"
        try:
            product_forms = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.column.main div.product-add-form"))
            )
            product_details['availableForSale'] = False  # Default value
            for form in product_forms:
                try:
                    button = form.find_element(By.CSS_SELECTOR,
                                               "div.fieldset div.actions button.action.primary.tocart span")
                    button_text = button.text.strip()
                    if "ADD TO CART" in button_text:
                        product_details['availableForSale'] = True
                        break
                except NoSuchElementException:
                    continue  # Just skip if the button is not found
        except (NoSuchElementException, TimeoutException) as e:
            print(f"No se puedo encontrar el elemento: 'availableForSale' :{e}")
            product_details['availableForSale'] = None

        ##########################################################
        "packSize"
        try:

            product_packSize_elements = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.column.main div.product-add-form"))
            )
            product_details['packSize'] = ''
            for item in product_packSize_elements:
                try:
                    element = item.find_element(By.CSS_SELECTOR, "div.fieldset span.dz-qty")
                    element_text = element.text.strip()
                    product_details['packSize'] = element_text if element_text else ''
                except NoSuchElementException:
                    product_details['packSize'] = ''
                    continue
        except (NoSuchElementException, TimeoutException) as e:
            print(f"No se puedo encontrar el elemento: 'packSize' :{e}")
            product_details['packSize'] = None

        ##########################################################
        "SKU"
        try:
            product_sku_elements = WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.product-info-stock-sku span.product-sku"))
            )
            if product_sku_elements:
                # match = re.search(r'\d+', product_sku[0].text)
                sku_text = product_sku_elements[0].text.strip()
                match = re.search(r'SKU\s*:\s*(\S+)', sku_text, re.IGNORECASE)
                if match:
                    # sku_number = match.group()
                    product_details['sku'] = match.group(1)
                    # product_details['sku'] = sku_number
                else:
                    print("No se encontró un formato válido de SKU en el texto.")
                    product_details['sku'] = None
        except (NoSuchElementException, TimeoutException) as e:
            print(f"No se puedo encontrar el elemento: 'sku' :{e}")
            product_details['sku'] = None

        ##################################################################
        "Capturar imágenes"
        images = []
        try:
            image_elements = soup.select("div.MagicToolboxSelectorsContainer a.mt-thumb-switcher")
            for image_element in image_elements:
                image_url = image_element.get('href')  # URL de la imagen en alta resolución
                thumbnail_url = image_element.find('img').get('src')  # URL del thumbnail
                images.append({'imagen': image_url})
                # Imprimir las URLs de las imágenes dentro del bucle
        except Exception as e:
            print(f"No se pudo encontrar las imágenes: {e}")

        product_details['images'] = images





    #####################################################################################################################
    # Extracting Detalis
        try:
            product_packing_element = soup.select("div.product.attribute.overview div.value[itemprop='description']")
            for attributes in product_packing_element:
                details = {}
                html_content = str(attributes)
                html_content = html_content.replace('<strong>', '|').replace('</strong>', '').replace('<br/>', '|')
                soup_cleaned = BeautifulSoup(html_content, 'html.parser')
                text = soup_cleaned.get_text(separator='|').split('|')

                for item in text:
                    if ':' in item:  # Asegurar que el item contiene una clave y valor
                        key, value = item.split(':', 1)
                        details[key.strip()] = value.strip()
                        #print(f"{key.strip()}: {value.strip()}")

                color = details.get('Color')
                size = details.get('Size')
                material = details.get('Material')
                productWeight = details.get('Weight')
                design = details.get('Design')
                packagingType = details.get('Packaging')

                product_details['color'] = color if color else None
                product_details['size'] = size if size else None
                product_details['productWeight'] = productWeight if productWeight else None
                product_details['material'] = material if material else None
                product_details['design'] = design if design else None
                product_details['packagingType'] = packagingType if packagingType else None



    ############# Realiza la copia y hace el recorrido del campo BuyMore #################################
                volume_prices = extract_volume_pricing(soup)
                entries = [product_details.copy()]

                for vp in volume_prices:
                    details = product_details.copy()
                    details['price']= vp['price']
                    details['quantity']= vp['quantity']
                    details['packSize'] =vp['unit']
                    entries.append(details)
                    # Imprimir cada entrada nueva
                if not entries[0]:  # Si el primer elemento está vacío, puede ser un indicativo de que no hay datos válidos
                    return None
                for entry in entries:
                     print("New Entry: ", entry)

                return entries

                if not any(product_details.values()):
                    product_details = None
        except (NoSuchElementException, TimeoutException) as e:
                product_details['color'] =  None
                product_details['size'] =  None
                product_details['productWeight'] =  None
                product_details['material'] =  None
                product_details['design'] =  None
                product_details['packagingType'] =  None
#####################################################################################################################

    except NoSuchElementException as e:
        print(f"No se pudo encontrar el elemento: {e}")
        return None
    except TimeoutException as e:
        print(f"Tiempo de espera excedido: {e}")
        return None


