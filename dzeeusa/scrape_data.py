from dzeeusa.common import(setup_driver,By,WebDriverWait,EC,TimeoutException,NoSuchElementException,json,params,pd,csv,datetime,ThreadPoolExecutor,as_completed,time)

from func.scraping_functions.collection_all_products import *
from func.scraping_functions.collection_url_category import *
from func.scraping_functions.scraping_products import *
# from func.processing_functions.scrapint_product_select import extract_categories_bathroom_Amenities
from params import HEADERS


################## SAVE CSV ########################

def save_urls_csv(urls, today_date_str):
    home_textiles_urls = getUrlHomeTextiles()

    # Crear DataFrames para ambos conjuntos de datos
    df_categories = pd.DataFrame(urls, columns=['url', 'text', 'level', 'parent_text'])
    df_textiles = pd.DataFrame(home_textiles_urls, columns=['url', 'text'])

    # Añadir columnas faltantes en df_textiles para que coincida con df_categories
    df_textiles['level'] = 'Nivel 2'  # o cualquier valor que tenga sentido
    df_textiles['parent_text'] = 'Home Textiles'  # o cualquier valor que tenga sentido

    # Concatenar ambos DataFrames
    df = pd.concat([df_categories, df_textiles], ignore_index=True, sort=False)

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

        df  = df.drop_duplicates()
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
    time.sleep(10)

def process_sublinks(sub_links):
    """Procesa una lista de sublinks extrayendo detalles de cada producto."""
    products_details = []
    processed_urls = set()  # Usamos un conjunto para almacenar los URLs procesados y evitar repeticiones.

    for link in sub_links:
        sub_link = link['url']  # Extraer la URL del diccionario
        sub_category = link['text']
        category = link['parent_text']

        product_details = get_url_list_products(sub_link,sub_category,category)
        if product_details:
            for product in product_details:
                product_url = product['url_products']
                if product_url not in processed_urls:
                    # Agrega el 'text' al detalle del producto
                   # product['category_text'] = link['text']
                    products_details.append(product)
                    processed_urls.add(product_url)
    # No hay impresión para URLs repetidos, se omiten silenciosamente.
    return products_details

def get_details_with_new_driver(url):
        # return get_details_products(driver, url)
        return getDetailsProducts(url)

################## Filter URL Category ########################
def filter_Display_levels(today_date_str):
    # Cargar los datos del CSV
    filepath = f'{params.COLLECTIONS_PATH_CATEGORIES}'
    df = pd.read_csv(filepath, sep='|')

    # Convertir la columna 'level' para facilitar el ordenamiento y filtrado
    df['level'] = df['level'].str.extract(r'(\d+)').astype(int)  # Extrae solo la parte numérica

    # Filtrar los datos para obtener solo los niveles 2 y 3
    filtered_data = df[df['level'].isin([2, 3])]

    # Verificar si el DataFrame filtrado está vacío
    if not filtered_data.empty:
        # Guardar el DataFrame filtrado en un archivo CSV, puedes añadir la fecha si es necesario al nombre del archivo
        save_urls_filter(filtered_data, today_date_str)
        #print("Datos filtrados guardados en:", filtered_data)
    else:
        print("No se obtuvieron URLs para guardar.")

################## Read to Collections path categorias ############################
def read_Categories_url_filter():
    filepath =f'{params.COLLECTIONS_PATH_CATEGORIES_FILTER}'
    df = pd.read_csv(filepath,sep="|")
    #print("Ruta del archivo:", df)
    #url_list = df['url'].tolist()
    url_list = df[['url', 'text','parent_text']].to_dict('records')
    #print(url_list)
    return url_list

def read_all_products(batch_size=40):
    filepath = f'{params.COLLECTIONS_PATH_PRODUCTS}'
    df = pd.read_csv(filepath, sep="|")
    for start in range(0, len(df), batch_size):
        batch = df.iloc[start:start + batch_size]
        yield [(row['url_products'], row['sub_category'],row['category']) for index, row in batch.iterrows()]


def read_categories_product_select():
    filepath =f'{params.COLLECTIONS_PATH_PRODUCTS}'
    df = pd.read_csv(filepath,sep="|")
    url_list = df[['url_products', 'category','sub_category']].to_dict('records')
    #Definimos la categoria
    needed_category  = ["Mikado Spa","Mikado Mist","Mikado Renaissances","Budgeted Soap & Shampoo","Make up Remover","Soap Dispensers"]
    #Filtramos
    filtered_cetegories = [category for category in url_list if category['sub_category'] in needed_category]

    return filtered_cetegories
############### MAIN #############################
def main():
    start_time = time.time()
    """Función principal que configura el driver, realiza el scraping y maneja la finalización."""
    driver = setup_driver()
    today_date_str = datetime.now().strftime('%Y_%m_%d')
    try:
        base_url = params.BASE_URL
        # ********************All Categories***********************************
        #scrapeGetUrlsCategory(driver, base_url,today_date_str)
        # ********************Filter Categories Nivel 2,3 /(0)***********************************
        #filter_Display_levels(today_date_str)
        # ********************All Products***********************************
        #sub_links_all_products = process_sublinks(read_Categories_url_filter())
        #save_all_to_products_csv(sub_links_all_products)
        # ******************* Read Products y Pasa los URLS *****************************
        # *******************************************************
        results = []
        for batch_urls in read_all_products():
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_product_details = {executor.submit(getDetailsProducts, url, sub_category,category): url for url,sub_category,category in batch_urls}

                for future in as_completed(future_to_product_details):
                    url = future_to_product_details[future]
                    try:
                        product_details_list = future.result()
                        if product_details_list:
                            results.extend(product_details_list)
                    except Exception as exc:
                        print(f"Error procesando {url}: {exc}")
                        results.append({'url': url, 'error': str(exc)})


            # # Guardar resultados en un archivo CSV
            df = pd.DataFrame(results, columns=params.HEADERS)
           # df = df.drop_duplicates()
            df.to_csv(f'{params.RAW_DATA_PATH}', index=False)
            print("Resultados guardados exitosamente.")
            time.sleep(60)
            save_failed_urls()

    finally:
        driver.quit()
    end_time = time.time()
    duration_seconds = end_time - start_time
    #Minutos
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    print(f"Tiempo de ejecución total: {int(minutes)} minutos y {seconds:.2f} segundos.")

if __name__ == "__main__":
    main()
