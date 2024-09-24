import re

import data_parameters as params

def clean_title(title,regex_list, key_words):
    
    if title:
        title = title.lower()
        for pattern in regex_list:
            title = re.sub(pattern, '', title)
        
        title = re.sub(r'&amp;', '&', title)

        for keys in key_words:
            for word in keys:
                title = re.sub(r'\b'+word.lower()+r'\b','', title)
        
        title = re.sub(r'\s+', ' ', title) # single spaces
        
        
    return title.title() if title else ''

def dimension_lwh_dict(match):
    if match:
        # Extract dimensions from the match
        dimensions = re.findall(r'\d+\.?\d*', match)
        dimensions = [float(dim) for dim in dimensions]

        # Determine the unit
        unit = ''
        if 'dia' in match.lower():
            unit = 'diameter'
        elif 'in' in match.lower() or '"' in match:
            unit = 'in'

        # Create the output dictionary
        output_dict = {
            'L': dimensions[0] if dimensions else '',
            'W': dimensions[1] if len(dimensions) > 1 else '',
            'H': dimensions[2] if len(dimensions) > 2 else '',
            'unit': unit
        }
        return output_dict
    else:
        return None

def extract_dimensions_from_title(title):

    if title:
        title = title.lower()
        # Define the regex patterns
        pattern1 = params.SIZE_REGEX_1
        pattern2 = params.SIZE_REGEX_2
        
        # Match the title with the patterns
        match_1 = re.search(pattern1, title)
        match_2 = re.search(pattern2, title)

        # Choose the appropriate match
        match = match_1 if match_1 else match_2
        
        return match.group() if match else None
   
def extract_num_from_text(raw_text):
    
    num = ''
    if raw_text:
        num_regex = r'\d+(\.\d+)?'
        clean_txt = re.search(num_regex, raw_text)
        if clean_txt:
            num = clean_txt.group(0)
    
    return num

def from_specs(row, name):

    for i in range(9):
        if (row[f"specs.{i}.name"] == name):
            return row[f"specs.{i}.value"].lower()


def get_attr_from_text(title, keywords_list):
    # Works for fields with Keyword list
    
    # found_keywords = [keyword for keyword in keywords_list if keyword.lower() in title.lower()]
    found_keywords = [keyword for keyword in keywords_list if re.search(r'\b' + keyword.lower() + r'\b', title.lower())]
    attr = ' '.join(found_keywords) if found_keywords else ''

    return attr

def get_match_from_text(text, pattern):
    
    text = text.lower()
    match = re.search(pattern, text)
    return match.group() if match else ''

def save_in_option(row, name, value):
    # Find the next available option.[i] index
    i = 0
    option_saved = False
    while not option_saved:
        if (f"option.{i}.name" in row.index or f"option.{i}.value" in row.index):
            option_name = row[f"option.{i}.name"]
            option_value = row[f"option.{i}.value"]
            if (option_name == "" and option_value == ""):
                row[f"option.{i}.name"] = name
                row[f"option.{i}.value"] = value
                option_saved = True
        else:
            row[f"option.{i}.name"] = name.title()
            row[f"option.{i}.value"] = value.title()
            option_saved = True
        i += 1
    return row

def set_product_value(df, row, keywords_list):
    
    values = []
    title = row['title']
    description = row['description']
    title_keywords = [keyword for keyword in keywords_list if re.search(r'\b' + keyword.lower() + r'\b', title.lower())]
    description_keywords = [keyword for keyword in keywords_list if re.search(r'\b' + keyword.lower() + r'\b', description.lower())]
    values = title_keywords[:]
    values.extend(description_keywords)
    values = list(set(values))

    if values:
        for num, value in enumerate(values):
            row[f'productValue.{num}'] = value.title()

    return row

def standardize_attr(attr, attr_formats):
    # Standardize attributes based on FORMATS defined on params
    stand_attr = ''
    if attr:
        attr = attr.lower()
        stand_attr = attr_formats[attr] if attr in attr_formats else attr
        
    return stand_attr

def standardize_volume(volume):
    
    if volume:
        clean_volume = volume.lower()
        clean_volume = re.sub(r'\b(?:ounces?|ounce|oz)\b', 'oz', clean_volume)
        clean_volume = re.sub(r'\b(?:liters?|lt)\b', 'l', clean_volume)
        clean_volume = re.sub(r'\b(?:quarts?|quart|qrts?|qt)\b', 'qt', clean_volume)
        clean_volume = re.sub(r'\b(?:gallons?|gallon|gal)\b', 'gal', clean_volume)
        clean_volume = clean_volume.replace(',', '')
        return clean_volume if volume != clean_volume else volume
