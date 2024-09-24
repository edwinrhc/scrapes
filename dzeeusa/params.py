import datetime
import os
import re

BASE_URL = 'https://dzeeusa.com'
COLLECTIONS_CATEGORIES = [
'hotel-towels.html', #Towel
'bed-sheets.html',  #Bedding
'top-of-bed.html',  #Top of bed
'room-essentials.html', #Room essentials
'hotel-amenities.html', #HouseKeeping
'promotion.html',   #Promotion
'shop-for-home.html'  #Home Textiles
]



TIMEOUT = 10
MIN_TIMEOUT = 10
MAX_TIMEOUT = 25

MIN_COLLECTION_SLEEP = 2
MAX_COLLECTION_SLEEP = 5

MIN_PRODUCT_SLEEP = 2
MAX_PRODUCT_SLEEP = 5

# Ruta !!!
DATA_PATH = '../dzeeusa/data'
# En caso que no exista la carpeta DATA
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)


# CREATE TIMESTAMP
today_date = datetime.date.today() # YYYY-MM-DD
today_date_str = today_date.strftime('%Y_%m_%d')



# PATH FILES
COLLECTIONS_PATH_CATEGORIES = f'{DATA_PATH}/{today_date_str}_collection_url_category.csv'
COLLECTIONS_PATH_CATEGORIES_FILTER = f'{DATA_PATH}/{today_date_str}_collection_url_filter_category.csv'
COLLECTIONS_PATH = f'{DATA_PATH}/{today_date_str}_collections_category.csv'
COLLECTIONS_PATH_PRODUCTS = f'{DATA_PATH}/{today_date_str}_collections_all_products.csv'

FAILED_URLS = f'{DATA_PATH}/´{today_date_str}_failed_urls.csv'


RAW_DATA_PATH = f'{DATA_PATH}/{today_date_str}_raw_data.csv'
PROCESSED_DATA_PATH = f'{DATA_PATH}/{today_date_str}_processed_data.csv'



###### New prod Template ######
HEADERS = [
    'uniqueIdentifier',
    'url',
    'availableForSale',
    'title',
    'description',
    'metaTitle',
    'metaDescription',
    'vendor',
    'manufacturerName',
    'brand',
    'model',
    'price',
    'vendorCategory.0',
    'vendorCategory.1',
    'vendorCategory.2',
    'vendorCategory.3',
    'categories.0',
    'categories.1',
    'material',
    'color',
    'approvedBy',
    'totalInventory',
    'images',
    'manufacturerNumber',
    'upc',
    'sku',
    'specifications',
    'options',
    'productMinOrderCases',
    'productMinOrderPrice',
    'caseSize',
    'packSize',
    'size',
    'stdSize',
    'productLength',
    'productWidth',
    'productHeight',
    'productWeight',
    'packageLength',
    'packageWidth',
    'packageHeight',
    'packageWeight',
    'shippingFrom',
    'shippingCost',
    'freeShipping',
    'certificationsAndStandards',
    'origin',
    'productValues',
    'canCustomize',
    'ourCost',
    'despensingType',
    'packagingType',
    'productForm',
    'scent',
    'volume',
    'border',
    'design',
    'shape',
    'towelType',
    'weightGSM',
    'feetPerRoll',
    'numberOfRolls',
    'numberOfSheets',
    'ply',
    'fit',
    'pattern',
    'threadCount',
    'pocketDepth',
    'ingredients',
    'itemForm',
    'microwaveSafe',
    'thickness',
    'categories'
]

categories_of_interest = {
    "Bed Sheets",
    "Pillows",
    "Mattress Pads",
    "Encasements",
    "Decorative Top Sheets",
    "Blankets",
    "Wraps & Skirts",
    "Hotel Comforter & Quilts",
    "Duvet Covers"
}

