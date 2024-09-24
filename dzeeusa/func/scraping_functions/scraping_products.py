from  dzeeusa.scrape_data import *
from dzeeusa.func.processing_functions.product_attributes_extractor import *
import requests
from bs4 import BeautifulSoup
import re
from requests.exceptions import HTTPError, RequestException
import math

def getDetailsProducts(product_detail_url, sub_category, category):
    """Obtiene y procesa los detalles del producto desde la URL dada usando solo requests y BeautifulSoup con reintento en caso de error 429."""
    max_retries = 5
    retry_delay = 10  # Comenzar con un retardo de 5 segundos

    for attempt in range(max_retries):
        try:
            response = requests.get(product_detail_url)
            response.raise_for_status()  # Esto lanzará una excepción si el código de estado es 4xx o 5xx
            # Si la respuesta es exitosa, parsea los datos
            soup = BeautifulSoup(response.text, 'html.parser')
            return parse_product_details(soup, product_detail_url, sub_category, category)
        except HTTPError as e:
            if e.response.status_code == 429:
                print(f"Demasiadas solicitudes, reintento {attempt + 1} de {max_retries} después de {retry_delay} segundos...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Aumentar el retardo exponencialmente
            else:
                print(f"HTTP error (status code {e.response.status_code}) fetching {product_detail_url}: {str(e)}")
                break  # Salir del loop si el error es diferente de 429
        except RequestException as e:
            print(f"Request error fetching {product_detail_url}: {str(e)}")
            break  # Salir del loop para errores de red, etc.
    return None  # Retorna None si todos los reintentos fallan

def extract_select_size_price(soup):
    size_price =  []
    select_element = soup.select_one(".admin__control-select")

    if select_element:
        for option in select_element.find_all("option")[1:]: #Se excluye el primer item
            value = option.get('value')
            price = option.get('price',0)
            text = option.text.strip()
            model = text.split('+')[0].strip()
            # Agrega un diccionario con los detalles de la opción a la lista
            size_price.append({'value': value, 'price': price,'ourCost':price, 'model': model})

    #print("Size Price: ",size_price)
    return size_price

def extract_volume_pricing(soup):
    """Extrae información de precios por volumen del HTML."""
    volume_prices = []
    volume_price_section = soup.select_one(".tierprice-section")
    if volume_price_section:
        price_rows = volume_price_section.select("tr")
        for row in price_rows:
            cells = row.select("td")
            for cell in cells:
                text = cell.get_text(strip=True)
                if '+' in text:
                    quantity = text.split('+')[0].strip()
                    price_text = cell.find('span', class_="font-bold").get_text(strip=True)
                    price_value = re.sub(r'[^\d.]', '', price_text)
                    price_unit = re.sub(r'[\d.$/]', '', price_text).strip()
                    volume_prices.append({'quantity': quantity, 'price': price_value, 'ourCost': price_value,'unit': price_unit})
    #print(volume_prices)
    return volume_prices


def extract_price_unit(soup):
    price_elements_span = soup.select("div.product-info-main span.special-price")
    price_elements_div = soup.select("div.product-info-main div.price-box.price-final_price")
    # Conjunto para rastrear las unidades ya vistas
    units_seen = set()
    # Lista para registrar todas las unidades capturadas
    unit_prices = []
    # Procesar elementos span.special-price
    for price_element in price_elements_span:
        price_cost_text_finish = price_element.text.strip()
        match = re.search(r'(?:/|per)\s*(\w+)', price_cost_text_finish)
        if match:
            # Capturando unidad
            unit = match.group(1).lower()
            if unit not in units_seen:
                units_seen.add(unit)
                unit_prices.append(unit)
    # Procesar elementos div.price-box.price-final_price
    for price_element in price_elements_div:
        price_cost_text_finish = price_element.text.strip()
        match = re.search(r'(?:/|per)\s*(\w+)', price_cost_text_finish)
        if match:
            # Capturando unidad
            unit = match.group(1).lower()
            if unit not in units_seen:
                units_seen.add(unit)
                unit_prices.append(unit)

    return unit_prices
###########################################################################################
def parse_product_details(soup,product_detail_url,sub_category,category):
    """Obtiene y procesa los detalles del producto desde la URL dada usando solo requests y BeautifulSoup."""
    try:
        response = requests.get(product_detail_url)
        response.raise_for_status()  # Esto lanzará una excepción si el código de estado es 4xx o 5xx
    except requests.exceptions.RequestException as e:
        handle_error(e,product_detail_url)
        return None

    # Inicializar variables
    title = None
    packagingType = None
    despensingType = None
    volume = None
    stdSize = None
    caseSize = None
    packSize = None
    availableForSale = None
    product_info = ""

    soup = BeautifulSoup(response.text, 'html.parser')

    product_name_element = soup.select_one(".product-info-main h1.page-title span.base")
    product_name =product_name_element.text.strip() if product_name_element else ""


    product_info_element  = soup.select_one(".product-info-main div.product.attribute.overview")
    product_info = product_info_element.text.strip() if product_info_element else ""

    "availableForSale"
    availableForSale ="ADD TO CART" in soup.select_one(
        "div.fieldset div.actions button.action.primary.tocart span").text.strip().upper() if soup.select_one(
        "div.fieldset div.actions button.action.primary.tocart span") else False



    # Seleccionar el contenedor principal con la clase 'product-info-main'
    product_info_main = soup.find('div', class_='product-info-main')
    # Dentro del contenedor 'product-info-main', buscar el elemento 'select' con el id 'qty'
    select_element = product_info_main.find('select', {'id': 'qty'}) if product_info_main else None
    # Buscar la primera opción dentro del elemento 'select'
    first_option = select_element.find('option') if select_element else None
    # Obtener el valor de la primera opción si existe y es un dígito
    min_order_element = first_option.get('value') if first_option and first_option.get('value').isdigit() else 1



    "title"
    title = product_name


    "caseSize"
    caseSize = int(min_order_element)
    #print("caseSize", caseSize)
    # case_size_from_title = sum_case_sizes(product_name)
    # case_size_from_details = sum_case_sizes(product_info)
    #
    # if case_size_from_title > 0:
    #     caseSize  = case_size_from_title
    # else:
    #     caseSize  = case_size_from_details



    "PackSize"
    packSize_element = soup.select_one(".product-info-main div.fieldset span.dz-qty")
    packSize_info = packSize_element.text.strip() if packSize_element else ""

    packSize_from_title = get_casePack_value(product_name)
    packSize_from_details = get_casePack_value(product_info)

    # Aplicar las condiciones para capturar todos los cambios de packSize
    unit_prices = extract_price_unit(soup)

    if packSize_info.lower() == "set":
        packSize = get_setPack_value(product_info)
    elif packSize_info.lower() == "case":
        if packSize_from_title > 0:
            packSize = packSize_from_title
        else:
            packSize = packSize_from_details
    else:
        packSize = get_packSize(unit_prices[0]) if unit_prices else None

    packSize = packSize_from_details


    category_select = "Bathroom Amenities"

    if isinstance(category, float):
        # Convertir a string
        category = str(category)

    if category and category_select  in category:
        "packagingType"
        packagingType = get_packaging_type(product_name)
        "despensingType"
        despensingType = get_dispensing_type(product_name)
        "volumeType"
        volume = get_volume(product_name)


    if(category in params.categories_of_interest):
        "stdSize"
        stdSize = get_stdSize_type(product_name)


    "Price"
    ### Price Wrapper
    price_cost_str = soup.select_one("div.product-info-main span.price-wrapper")['data-price-amount'] if soup.select_one("span.price-wrapper") else None
    price_finish = float(price_cost_str)
    price = caseSize * price_finish


    "OurCost"
    our_cost_str  = soup.select_one("span.price-wrapper[data-price-type='finalPrice']")['data-price-amount'] if soup.select_one("span.price-wrapper[data-price-type='finalPrice']") else None
    ourCost_finish = float(our_cost_str)
    ourCost = caseSize * ourCost_finish

    "productMinOrderCase MQO"
    #Regla -> Case Pack / MinQuantity
    if min_order_element:
        min_order_cases_int = int(min_order_element)

        if (caseSize > min_order_cases_int):
            MOQ = caseSize / min_order_cases_int
        else:
            MOQ = min_order_cases_int / caseSize

        min_order_cases = math.ceil(MOQ)
        #print("MQO:", min_order_cases)
    else:
        print("No se puedo encontrar el valor minimo")

    "productMinOrderPrice"
    productMinOrderPriceResult = min_order_cases * price
    productMinOrderPriceResult =  price
    productMinOrderPrice = round(productMinOrderPriceResult,2)
    if productMinOrderPrice == int(productMinOrderPrice):
        formattedMinOrderPrice = f"{int(productMinOrderPrice)}"
    else:
        formattedMinOrderPrice =f"{productMinOrderPrice:.2f}"


    product_details = {
        'url':product_detail_url,
        'vendor': soup.select_one("div.header.content a.logo")['title'] if soup.select_one("div.header.content a.logo") else None,
        'title': title,
        'metaTitle': soup.select_one("h1.page-title span.base").text.strip() if soup.select_one("h1.page-title span.base") else None,
        'price': price,
        'ourCost': ourCost,
        'description': ' '.join([li.text.strip() for li in soup.select("div.product.attribute.description li")]),
        'metaDescription': ' '.join([li.text.strip() for li in soup.select("div.product.attribute.description li")]),
        'availableForSale': availableForSale,
        'sku': re.search(r'SKU\s*:\s*(\S+)', soup.select_one("div.product-info-stock-sku span.product-sku").text.strip(), re.IGNORECASE).group(1) if soup.select_one("div.product-info-stock-sku span.product-sku") else None,
        'productMinOrderCases': min_order_cases,
        'productMinOrderPrice': formattedMinOrderPrice,
        'vendorCategory.0': category,
        'vendorCategory.1': sub_category,
        'packagingType':packagingType,
        'despensingType': despensingType,
        'volume':volume,
        'images': [img['href'] for img in soup.select("div.MagicToolboxSelectorsContainer a.mt-thumb-switcher") if 'href' in img.attrs],
        'packSize': packSize,
        'stdSize':stdSize,
        'caseSize':caseSize

    }
    # Additional attribute processing
    product_packing_element = soup.select("div.product.attribute.overview div.value[itemprop='description']")
    details = {}
    stdSizes = []

    for attributes in product_packing_element:
        details = {}
        html_content = str(attributes)
        html_content = html_content.replace('<strong>', '|').replace('</strong>', '').replace('<br/>', '|')
        soup_cleaned = BeautifulSoup(html_content, 'html.parser')
        text = soup_cleaned.get_text(separator='|').split('|')
        for item in text:
            if ':' in item:
                key, value = item.split(':', 1)
                #Procesamos la clave Size
                if key.strip() == 'Size':
                    # Regex mejorada para capturar solo medidas estrictas
                    pattern = r'\b(\d+)\s*[xX]\s*(\d+)(?:\s*[xX]\s*(\d+))?\b'
                    matches = re.findall(pattern, value)
                    cleaned_sizes = [' x '.join(filter(None, m)) for m in matches]
                    details[key.strip()] = ', '.join(cleaned_sizes)
                    text_without_sizes = re.sub(pattern, '', value).strip()
                    text_without_sizes = re.sub(r'\s*-\s*', ' ', text_without_sizes).strip()
                    if text_without_sizes:
                        stdSizes.append(text_without_sizes)
                else:
                    if key.strip().lower() == 'weight':
                        # Verifica si el valor de weight incluye 'GSM'
                        gsm_value = get_gsm_value(value)
                        if gsm_value:
                            # Si se encuentra GSM, asigna el valor a weightGSM
                            details['weightGSM'] = gsm_value
                        else:
                            # Si no, lo asigna a productWeight
                            details['productWeight'] = value.strip()

                    else:
                        details[key.strip()] = value.strip()
        stdSizes = [re.sub(r"[\[\]'']+", '', s).strip() for s in stdSizes]
        stdSizes_text = ', '.join(stdSizes)
        product_details.update({
            'color': details.get('Color',''),
            'size': details.get('Size',''),
            'productWeight': details.get('Weight',''),
            'material': details.get('Material',''),
            'design': details.get('Design',''),
            'weightGSM': details.get('weightGSM', '')
        })

    # Lista de entradas que incluirá tanto precios por tamaño como por volumen
    entries = [product_details.copy()]

    # Procesar 'select size' y añadir a las entradas
    select_size_price = extract_select_size_price(soup)
    for sel in select_size_price:
        select_details = product_details.copy()
        ourCostSize = float(sel['ourCost']) if 'ourCost' in sel and sel['ourCost'] is not None else 0.0
        total_cost = price + ourCostSize
        Selectmin_order_cases = min_order_cases * total_cost
        Selectmin_order_cases_rounded = round(Selectmin_order_cases, 2)
        # Formatear para remover decimales innecesarios
        if Selectmin_order_cases_rounded == int(Selectmin_order_cases_rounded):
            formatted_min_order_price = f"{int(Selectmin_order_cases_rounded)}"
        else:
            formatted_min_order_price = f"{Selectmin_order_cases_rounded:.2f}"

        select_details.update({
            'price': total_cost,
            'productMinOrderPrice':formatted_min_order_price,
            'ourCost':total_cost,
            'value': sel['value'],  # Asegúrate de que 'value' y 'model' son relevantes para tus HEADERS
            'model': sel['model']
        })
        entries.append(select_details)

    "Volumen"
# Procesar 'volumen por precio' y añadir a las entradas
    volume_prices = extract_volume_pricing(soup)
    formatted_ranges = []

    # Filtrar y ordenar por cantidad cuando esté disponible
    volume_prices = [vp for vp in volume_prices if 'quantity' in vp and vp['quantity'].isdigit()]
    volume_prices.sort(key=lambda x: int(x['quantity']))

    # Crear rangos
    for i, vp in enumerate(volume_prices):
        quantity = int(vp['quantity'])
        uni = vp['unit']
        if i == 0:
          #  formatted_ranges.append(f"(Buying Quantity, >= {quantity})")
            formatted_ranges.append(f"(Buying Quantity,  {quantity}+ {uni})")
        else:
            previous_quantity = int(volume_prices[i - 1]['quantity'])
          #  formatted_ranges.append(f"(Buying Quantity, {previous_quantity + 1} <= x <= {quantity})")
            formatted_ranges.append(f"(Buying Quantity, {quantity}+ {uni})")
    if volume_prices:  # Añadir un rango extra solo si hay precios disponibles
       # formatted_ranges.append(f"(Buying Quantity, > {volume_prices[-1]['quantity']})")
        formatted_ranges.append(f"(Buying Quantity,  {volume_prices[-1]['quantity']})")
        for i, vp in enumerate(volume_prices):
            volume_details = product_details.copy()
            ourCost = float(vp['ourCost']) if 'ourCost' in vp and vp['ourCost'] is not None else 0.0
            price_range = float(vp['price'])
            quantity = int(vp['quantity'])
            total_price = price_range * quantity
            caseSize_Range = int(vp['quantity'])
            volumen_select = ourCost * quantity
            volumen_select_rounded = round(volumen_select, 2)
            formatted_volumen_price = f"{int(volumen_select_rounded)}" if volumen_select_rounded == int(
                volumen_select_rounded) else f"{volumen_select_rounded:.2f}"

            range_description = formatted_ranges[i]  # Usar índice seguro, ya que se ha filtrado

            if min_order_element:
                min_order_cases_int = int(min_order_element)
                if (caseSize_Range > min_order_cases_int):
                    MOQ = caseSize_Range / min_order_cases_int
                else:
                    MOQ = min_order_cases_int / caseSize_Range
                min_order_cases_int = math.ceil(MOQ)

            if packSize_info.lower() == "set":
                packSize = get_setPack_value(product_info)
            else:
                packiSize = get_packSize(vp['unit'])

            volume_details.update({
                'price': total_price,
                'productMinOrderPrice': formatted_volumen_price,
                'ourCost': volumen_select,
                'caseSize':vp['quantity'],
                'productMinOrderCases':min_order_cases_int,
                'packSize': packSize,
                'options': range_description
            })
            entries.append(volume_details)

    return entries


def handle_error(e,url):
    if isinstance(e,requests.exceptions.HTTPError):
        error_msg =f"HTTP error (status code {e.response.status_code}) fetching {url}:{e}"
    elif isinstance(e, requests.exceptions.ConnectionError):
        error_msg=f"Connection error fetching {url}: {e}"
    elif isinstance(e, requests.exceptions.Timeout):
        error_msg=f"Timeout error fetching {url}: {e}"
    else:
        error_msg=f"General request error fetching {url}: {e}"
    print(error_msg)
    failed_urls.append({'url': url, 'error': error_msg})

failed_urls = []

def save_failed_urls():
    """Guarda los URLs fallidos en un archivo CSV."""
    with open('failed_urls.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Failed URLs'])
        for url in failed_urls:
            writer.writerow([url])
