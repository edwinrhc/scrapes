def extract_title(soup):
    """Function to extract the product title"""
    title = soup.find('span', class_='description-title')
    if title:
        return title.text
    return ""

def extract_description(soup):
    """Function to extract the product description"""
    description = soup.find('p', class_='product-story')
    if description:
        return description.text
    return ""

def extract_sub_descriptions(soup):
    """Function to extract the product sub descriptions"""
    sub_descriptions = soup.find_all('span', class_='sub-description')
    if sub_descriptions:
        return [sub.text for sub in sub_descriptions]
    else:
        return ["", "", ""]

def extract_price_stock(soup):
    """Function to extract the product price"""
    main_div = soup.find('form', class_='order-container')
    spans = main_div.find_all('span', class_='ng-star-inserted') if main_div else None
    if spans:
        return [spans[0].text, spans[1].text]
    return ["", ""]

def extract_upcs(soup):
    """Function to extract the products upc"""
    div_svgs = soup.find_all('div', class_='upc-box ng-star-inserted')
    box_upc = ""
    retail_upc = ""
    unit_upc = ""
    if div_svgs:
        for div in div_svgs:
            title_div = div.find('div', class_='mat-title')
            title = title_div.text.strip().lower() if title_div else ""
            svg = div.find('svg')
            if title == "caja upc":
                box_upc = svg['jsbarcode-value'] if svg else ""
            elif title == "retail upc":
                retail_upc = svg['jsbarcode-value'] if svg else ""
            elif title == "unit upc":
                unit_upc = svg['jsbarcode-value'] if svg else ""
    return [box_upc, retail_upc, unit_upc]


def extract_images(soup):
    """Function to extract the product images"""
    outer_div = soup.find('div', class_='carousel-outer-wrapper')
    images = outer_div.find_all('img', class_='carouselItem') if outer_div else None
    if images:
        return [image['src'] for image in images]
    return ""

def extract_volume(soup):
    """Function to extract the product volume"""
    main_div = soup.find('div', class_='cdk-overlay-pane')
    inner_div = main_div.find('div', class_='nutrition-header') if main_div else None
    if inner_div:
        spans = inner_div.find_all('span')
        if len(spans) > 1:
            return spans[1].text
    return ""

def extract_ingredients(soup):
    """Function to extract the product ingredients"""
    main_div = soup.find('div', class_='cdk-overlay-pane')
    inner_div = main_div.find('div', class_='ingredients ng-star-inserted') if main_div else None
    if inner_div:
        spans = inner_div.find_all('span')
        if len(spans) > 1:
            return spans[1].text
    return ""

def extract_product_value(soup):
    """Function to extract the product values"""
    mat_chip_list = soup.find('mat-chip-list', class_='mat-chip-list')
    wrapper = mat_chip_list.find('div', class_='mat-chip-list-wrapper') if mat_chip_list else None
    if wrapper:
        values_divs = wrapper.find_all('div', class_='dietary-field ng-star-inserted')
        values = [div.find('span').text.strip() for div in values_divs] if values_divs else ""
        return values
    return ""

def save_url_in_csv(url):
    """Function to save url in .csv"""
    with open('data/scraped/error_url.csv', 'a') as file:
        file.write(f"{url}\n")
