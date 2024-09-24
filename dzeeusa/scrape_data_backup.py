from dzeeusa.common import(setup_driver,By,WebDriverWait,EC,TimeoutException,NoSuchElementException,json,params,pd,csv,datetime,ThreadPoolExecutor,as_completed)
from func.scraping_functions.collection import *
from func.scraping_functions.collection_all_products import *
from func.scraping_functions.collection_url_category import *
from params import HEADERS
################## SAVE CSV ########################
def save_urls_csv(urls, today_date_str):
    """Guarda la jerarquía de categorías en un archivo CSV."""
    # Crear un DataFrame a partir de los datos
    df = pd.DataFrame(urls, columns=['url', 'text', 'level'])

    # Convertir la columna 'level' para facilitar el ordenamiento
    df['level'] = df['level'].str.extract(r'(\d+)').astype(int)  # Uso de raw string para evitar SyntaxWarning

    # Ordenar el DataFrame por la columna 'level'
    df = df.sort_values(by='level')

    # Construir el nombre del archivo con la ruta y la fecha
    filepath = f'{params.COLLECTIONS_PATH_CATEGORIES}'

    # Guardar el DataFrame en un archivo CSV sin índice y con el separador "|"
    df.to_csv(filepath, index=False, sep="|")
    print("Ruta del archivo:", filepath)

def save_urls_filter(filtered_data, today_date_str):
    """Guarda la jerarquía de categorías en un archivo CSV."""
    # Crear un DataFrame a partir de los datos
    filtered_data = filtered_data.sort_values(by='level')
    # Construir el nombre del archivo con la ruta y la fecha
    filepath = f'{params.COLLECTIONS_PATH_CATEGORIES_FILTER}'
    filtered_data.to_csv(filepath, index=False, sep="|")
    print("Ruta del archivo:", filepath)


def save_hierarchy_to_csv(hierarchy, today_date_str):
    """Guarda la jerarquía de categorías en un archivo CSV."""
    df = pd.DataFrame(hierarchy)
    filepath = f'{params.COLLECTIONS_PATH}'
    df.to_csv(filepath, index=False, sep="|")
    print("Ruta del archivo:", filepath)

def save_all_to_products_csv(product_details):
    """Guarda los detalles de los productos en un archivo CSV."""
    if product_details:
        # Crear un DataFrame de pandas con la lista de diccionarios
        df = pd.DataFrame(product_details)
        # Definir la ruta del archivo CSV
        filepath = f'{params.COLLECTIONS_PATH_PRODUCTS}'
        # Guardar el DataFrame en un archivo CSV
        df.to_csv(filepath, index=False, sep="|")
        print(f"Ruta del archivo de productos guardado: {filepath}")
    else:
        print("No hay detalles de productos para guardar.")

################## Get URL Category ########################
def scrapeGetUrlsCategory(driver, base_url,today_date_str):
    urls = getUrlsCategory(driver, base_url)
    if urls:  # Verificar si se obtuvo alguna URL
        save_urls_csv(urls, today_date_str)
    else:
        print("No se obtuvieron URLs para guardar.")

def process_sublinks(driver, sub_links):
    """Procesa una lista de sublinks extrayendo detalles de cada producto."""
    products_details = []
    processed_urls = set()  # Usamos un conjunto para almacenar los URLs procesados y evitar repeticiones.

    for sub_link in sub_links:
        product_details = get_url_list_products(driver, sub_link)
        if product_details:
            for product in product_details:
                product_url = product['url_products']
                if product_url not in processed_urls:
                    # Imprime cada URL procesada (opcional, quitar si deseas un proceso totalmente silencioso)
                    # print(product_url)
                    products_details.append(product)
                    processed_urls.add(product_url)
                # No hay impresión para URLs repetidos, se omiten silenciosamente.

    return products_details


def get_details_with_new_driver(url):
    with webdriver_context() as driver:
        return get_details_products(driver, url)


################## Filter URL Category ########################
def filter_Display_levels(today_date_str):
    # Cargar los datos del CSV
    df = pd.read_csv(f'{params.COLLECTIONS_PATH_CATEGORIES}', sep='|')
    # Filtrar los datos para obtener solo los niveles 2 y 3
    filtered_data = df[df['level'].isin([2, 3]) | ((df['level']==0) & (df['text'].str.contains('Home Textiles')))]
    # Usar .empty para verificar si el DataFrame filtrado está vacío
    if not filtered_data.empty:
        save_urls_filter(filtered_data, today_date_str)  # Asegúrate de llamar a la función correcta
    else:
        print("No se obtuvieron URLs para guardar.")

################## Read to Collections path categorias ############################
def read_Categories_url_filter():
    filepath =f'{params.COLLECTIONS_PATH_CATEGORIES_FILTER}'
    df = pd.read_csv(filepath,sep="|")
    #print("Ruta del archivo:", df)
    url_list = df['url'].tolist()
    #print(url_list)
    return url_list

def read_all_products():
    filepath =f'{params.COLLECTIONS_PATH_PRODUCTS}'
    df = pd.read_csv(filepath,sep="|")
    #print("Ruta del archivo:", df)
    url_list = df['url_products'].tolist()
    #print(url_list)
    return url_list
############### MAIN #############################
def main():
    """Función principal que configura el driver, realiza el scraping y maneja la finalización."""
    driver = setup_driver()
    today_date_str = datetime.now().strftime('%Y_%m_%d')  # Definir today_date_str aquí para uso global
    try:
        base_url = params.BASE_URL  # Asegúrate de definir esto en tu módulo de parámetros

        # ********************All Categories***********************************
        #scrapeGetUrlsCategory(driver, base_url,today_date_str)
        # ********************Filter Categories Nivel 2,3 /(0)***********************************
        #filter_Display_levels(today_date_str)
        # ********************All Products***********************************
        #sub_links_all_products = process_sublinks(driver, read_Categories_url_filter())
        #save_all_to_products_csv(sub_links_all_products)
        # ******************* Read Products y Pasa los URLS *****************************
        all_products = read_all_products()
        # *******************************************************
        results = []
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     future_to_url = {executor.submit(get_details_with_new_driver, url): url for url in
        #                      all_products}
        #
        #     for future in as_completed(future_to_url):
        #         url = future_to_url[future]
        #         try:
        #             product_details = future.result()  # Ahora un diccionario
        #             if product_details:  # Verifica si el diccionario no está vacío
        #                 # Verificar si todas las claves necesarias están en el diccionario
        #                 if all(key in product_details for key in
        #                        ['title', 'description', 'metaTitle', 'metaDescription', 'availableForSale', 'vendor',
        #                         'price', 'sku', 'size', 'color', 'productWeight', 'material', 'design','packagingType','packSize']):
        #                     results.append({
        #                         'url': url,
        #                         'title': product_details['title'],
        #                         'description': product_details['description'],
        #                         'metaTitle': product_details['metaTitle'],
        #                         'metaDescription': product_details['metaDescription'],
        #                         'availableForSale': product_details['availableForSale'],
        #                         'vendor': product_details['vendor'],
        #                         'price': product_details['price'],
        #                         'sku': product_details['sku'],
        #                         'size': product_details['size'],
        #                         'color': product_details['color'],
        #                         'productWeight': product_details['productWeight'],
        #                         'material': product_details['material'],
        #                         'design': product_details['design'],
        #                         'packagingType': product_details['packagingType'],
        #                          'packSize':product_details['packSize']
        #
        #                     })
        #                 else:
        #                     # Manejar el caso donde algunos datos no estén disponibles
        #                     results.append({
        #                         'url': url,
        #                         'title': product_details.get('title', None),
        #                         'description': product_details.get('description', None),
        #                         'metaTitle': product_details.get('metaTitle', None),
        #                         'metaDescription': product_details.get('metaDescription', None),
        #                         'availableForSale': product_details.get('availableForSale', None),
        #                         'vendor': product_details.get('vendor', None),
        #                         'price': product_details.get('price', None),
        #                         'sku': product_details.get('sku', None),
        #                         'size': product_details.get('size', None),
        #                         'color': product_details.get('color', None),
        #                         'productWeight': product_details.get('productWeight', None),
        #                         'material': product_details.get('material', None),
        #                         'design': product_details.get('design', None),
        #                         'packagingType': product_details.get('packagingType', None),
        #                         'packSize': product_details.get('packSize', None)
        #                     })
        #         except Exception as exc:
        #             print(f"Error procesando {url}: {exc}")
        #             results.append({
        #                 'url': url,
        #                 'title': None,
        #                 'availableForSale': None,
        #                 'vendor': None
        #             })
        #
        # # Guardar resultados en un archivo CSV
        # df = pd.DataFrame(results, columns=params.HEADERS)
        # df.to_csv(f'{params.RAW_DATA_PATH}_results.csv', index=False)
        # print("Resultados guardados exitosamente.")

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(get_details_with_new_driver, url): url for url in all_products}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    product_details_list = future.result()  # Esto ahora es una lista de diccionarios

                    if product_details_list:
                        for product_details in product_details_list:
                            # Añade una entrada para cada diccionario en la lista
                            results.append({
                                'url': url,
                                'title': product_details.get('title', ""),
                                'description': " ".join(product_details.get('description', [])),
                                'metaTitle': product_details.get('metaTitle', ""),
                                'metaDescription': " ".join(product_details.get('metaDescription', [])),
                                'availableForSale': product_details.get('availableForSale', ""),
                                'vendor': product_details.get('vendor', ""),
                                'price': product_details.get('price', ""),
                                'sku': product_details.get('sku', ""),
                                'size': product_details.get('size', ""),
                                'color': product_details.get('color', ""),
                                'productWeight': product_details.get('productWeight', ""),
                                'material': product_details.get('material', ""),
                                'design': product_details.get('design', ""),
                                'packagingType': product_details.get('packagingType', ""),
                                'packSize': product_details.get('packSize', ""),
                                'images':product_details.get('images',"")

                            })
                except Exception as exc:
                    print(f"Error procesando {url}: {exc}")
                    results.append({
                        'url': url,
                        'title': None,
                        'availableForSale': None,
                        'vendor': None
                    })

        # # Guardar resultados en un archivo CSV
        df = pd.DataFrame(results, columns=params.HEADERS)
        df.to_csv(f'{params.RAW_DATA_PATH}_results.csv', index=False)
        print("Resultados guardados exitosamente.")


    finally:
        driver.quit()


if __name__ == "__main__":
    main()
