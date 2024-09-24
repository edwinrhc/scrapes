""" Here are all paths parameters """



# LOGIN
LOGIN_URL = 'https://login.vtinfo.com/adfs/oauth2/authorize/?client_id=deeb6927-e324-44e8-b7d8-7de363af8243&redirect_uri=http://apps.vtinfo.com/retailer-portal/openid&resource=https://vtinfo.com&response_type=code&scope=email%20profile%20vtinfo.roles%20vtinfo.itemcatalog.distributor.read%20vtinfo.beverage.retailer.pricing&state=sA8kps'

# PRODUCTS SCRAPING
LANDING_BASE_URL = 'https://apps.vtinfo.com'
PRODUCTS_LINKS_PATH = 'data/scraped/products_links.csv'
PRODUCTS_LINKS_PATH_2 = 'data/scraped/products_links_v2.csv'
LANDING_HTML_PATH = 'data/html/landing.html'
PRODUCT_CSV_PATH = 'data/scraped/products.csv'

# PRODUCTS PROCESSING
FINAL_PRODUCTS_PATH = 'data/processed/products.csv'
FINAL_PRODUCTS_PATH_EXCEL = 'data/processed/products.xlsx'
