
from pactex.common import(setup_driver,By,WebDriverWait,EC,TimeoutException,NoSuchElementException,json,params,pd,csv,datetime,ThreadPoolExecutor,as_completed,time)

from func.scraping_functions.scraping_url_collection_products import *
from func.scraping_functions.scraping_url_category import *
from func.scraping_functions.scraping_products import *
from func.scraping_functions.scraping_url_sub_category import *
from func.scraping_functions.scraping_url_sub_sub_category import *
# from func.processing_functions.scrapint_product_select import extract_categories_bathroom_Amenities
from params import HEADERS

############################## SAVE CSV ##############################
def save_urls_csv(urls, today_date_str):
    """Guarda la jerarquía de categorías en un archivo CSV."""
    df = pd.DataFrame(urls, columns=['url', 'category'])
    filepath = f'{params.COLLECTIONS_PATH_CATEGORIES}'
    df.to_csv(filepath, index=False, sep="|")
    print("Ruta del archivo:", filepath)

def save_all_sub_category(product_details):
    if product_details:
        df = pd.DataFrame(product_details)
        filepath = f'{params.COLLECTIONS_PATH_SUB_CATEGORIES}'
        df.to_csv(filepath,index=False, sep="|")
        print(f"Ruta del archivo de productos guardado: {filepath}")
    else:
        print("No hay detalles de productos para guardar.")




 ############ GET URL CATEGORY ######################
def scrape_url_category(driver, base_url, today_date_str):
    urls = get_url_category(driver, base_url)
    if urls:  # Verificar si se obtuvo alguna URL
        save_urls_csv(urls, today_date_str)
    else:
        print("No se obtuvieron URLs para guardar.")
    time.sleep(10)



################## READ URL CATEGORY ###################
def read_url_sub_category():
    filepath = f'{params.COLLECTIONS_PATH_CATEGORIES}'
    df = pd.read_csv(filepath, sep="|")
    return df[['url', 'category']].to_dict('records')


################### Process ##########################
def process_sub_category(sub_links):
    products_details = []
    processed_urls = set()
    for link in sub_links:
        product_url = link['url']
        product_text = link['category']
        #parent_text = link.get('parent_text', '')  # Usamos get para manejar casos donde parent_text puede no estar presente
        if product_url not in processed_urls:
            product_details = get_url_sub_category(product_url, product_text)
            if product_details:
                products_details.extend(product_details)
                processed_urls.add(product_url)
    return products_details


def main():
    start_time = time.time()
    """Función principal que configura el driver, realiza el scraping y maneja la finalización."""
    driver = setup_driver()
    today_date_str = datetime.now().strftime('%Y_%m_%d')
    try:
        base_url = params.BASE_URL
        # ********************All Categories***********************************
        # scrape_url_category(driver, base_url, today_date_str)
        # ********************Sub Category***********************************
        # sub_links = read_url_sub_category()
        # results = process_sub_category(sub_links)
        # save_all_sub_category(results)

        # get_url_collection()
        collections = get_url_sub_sub_collection()

        # ********************All Products***********************************
        #sub_links_all_products = process_sublinks(read_Categories_url_filter())
        #save_all_to_products_csv(sub_links_all_products)
        # ******************* Read Products y Pasa los URLS *****************************
        # *******************************************************
        #results = []
        # for batch_urls in read_all_products():
        #     with ThreadPoolExecutor(max_workers=5) as executor:
        #         future_to_product_details = {executor.submit(getDetailsProducts, url, sub_category, category): url
        #                                      for url, sub_category, category in batch_urls}
        #
        #         for future in as_completed(future_to_product_details):
        #             url = future_to_product_details[future]
        #             try:
        #                 product_details_list = future.result()
        #                 if product_details_list:
        #                     results.extend(product_details_list)
        #             except Exception as exc:
        #                 print(f"Error procesando {url}: {exc}")
        #                 results.append({'url': url, 'error': str(exc)})
        #
        #     # # Guardar resultados en un archivo CSV
        #     df = pd.DataFrame(results, columns=params.HEADERS)
        #     # df = df.drop_duplicates()
        #     df.to_csv(f'{params.RAW_DATA_PATH}', index=False)
        #     print("Resultados guardados exitosamente.")
        #     time.sleep(60)
        #     save_failed_urls()

    finally:
        driver.quit()
    end_time = time.time()
    duration_seconds = end_time - start_time
    # Minutos
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    print(f"Tiempo de ejecución total: {int(minutes)} minutos y {seconds:.2f} segundos.")

if __name__ == "__main__":
    main()
