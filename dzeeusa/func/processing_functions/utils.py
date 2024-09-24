import re
import params as params

# Function to extract and refine model names
def extract_model_name(title, model_keywords):
    # Remove text within parentheses
    title_cleaned = re.sub(r"\(.*?\)", "", title).strip()
    # Find keywords in the title
    found_keywords = [keyword for keyword in model_keywords if keyword.lower() in title_cleaned.lower()]
    # Construct model name based on found keywords or create a custom model name
    if found_keywords:
        model_name = ' '.join(found_keywords)
    else:
        words = title_cleaned.split()
        model_name = ' '.join(words[:2]) if len(words) >= 2 else title_cleaned
    return model_name

# Function to standardize model names (capitalize each word and exclude explicit sizes)
def standardize_model_name(model_name):
    try:
        if re.search(r'\d+(\.\d+)?\s*(oz\.|x|inch|"|cm|mm)', model_name.lower()):
            return ""  # Return blank for model names with explicit sizes
        return ' '.join(word.capitalize() for word in model_name.split())
    except Exception as e:
        print(f"Error standardizing model name: {model_name}")
        print(e)
        return ""

# Assign best-fit model to each product based on its title and category
def assign_best_fit_model(title, model_names):
    for model_name in model_names:
        if model_name.lower() in title.lower():
            return model_name
    return ""

# Function to save in option attribute
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
            row[f"option.{i}.name"] = name
            row[f"option.{i}.value"] = value
            option_saved = True
        i += 1

# Function to save in specs attribute
def save_in_specs(row, name, value):
    # Find the next available option.[i] index
    i = 0
    specs_saved = False
    while not specs_saved:
        if (f"specs.{i}.name" in row.index or f"specs.{i}.value" in row.index):
            specs_name = row[f"specs.{i}.name"]
            specs_value = row[f"specs.{i}.value"]
            if (specs_name == "" and specs_value == ""):
                row[f"specs.{i}.name"] = name
                row[f"specs.{i}.value"] = value
                specs_saved = True
        else:
            row[f"specs.{i}.name"] = name
            row[f"specs.{i}.value"] = value
            specs_saved = True
        i += 1

# Function to extract package details from product titles
def get_package(title, row, pattern):
    # Replace ” and “ with "
    title = title.replace("”", "\"").replace("“", "\"")

    # Search for packaging details in the title
    match = re.search(pattern, title)
    if match:
        # Extract N_PACKAGE and PACKAGE_TYPE
        n_package, separator, package_type = match.groups()

        # Set package details to the row
        save_in_option(row, package_type, n_package)
        row['caseSize'] = 1
        row['packSize'] = n_package

        # Remove the matched pattern from the title
        title = re.sub(pattern, "", title).strip()

        # Return in title formmat
        return title.title()
    return title

# Function to format & clean parragraphs
def format_parragraphs(parragraphs):
    final_text = ""
    for parragraph in parragraphs:
        sentences = parragraph.split(".")
        sentences = map(lambda x: x.strip().capitalize(), sentences)
        parragraph = ". ".join(sentences)
        final_text += parragraph + "\n"
    return final_text

# Function to clean a text
def clean_text(text):
    '''Removes special characters, weird symbols,
    emojis and extra spaces from a text'''
    # Replace ” and “ with "
    text = text.replace("”", "\"").replace("“", "\"")

    # Remove special characters and symbols
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) # Remove non-ASCII characters

    # Remove emojis
    # Wide UCS-4 build
    emoji_pattern = re.compile(
        u"["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Format the text
    parragraphs = text.split("\n")
    text = format_parragraphs(parragraphs)
    return text

# Function to extract the size from the description
def extract_size_from_description(row):
    # Extract Size from title
    title_match = re.search(params.DIMENSION_REGEX, row['metaTitle'])
    if title_match:
        # Extract the size
        size = title_match.group(0)

        # Save the size in option
        save_in_option(row, "Size", size)
    else:
        description_match = re.search(params.DIMENSION_REGEX, row['description'])
        if description_match:
            # Extract the size
            size = description_match.group(0)

            # Save the size in option
            save_in_option(row, "Size", size)
    return row

# Function to extract material from the description
def extratact_material_from_description(row):
    material_matches = re.findall(params.MATERIAL_REGEX, row['description'])
    if material_matches:
        material_list = [list(material) for material in material_matches]
        flattened_list = [item for sublist in material_list for item in sublist]
        final_material_list = list(set(flattened_list))
        final_material_list = list(map(lambda x: x.capitalize(), final_material_list))
        material = ', '.join(final_material_list)
        row['material'] = material
    else:
        row['material'] = 'Bamboo'
    return row

# Function to extract the volume of the product
def extract_volume_from_description(row):
    # Extract volume from title
    title_matches = re.findall(params.VOLUME_REGEX, row['metaTitle'], flags=re.IGNORECASE)
    if title_matches:
        setted_list = list(set(title_matches))
        for match in setted_list:
            # Save the volume in specs
            save_in_specs(row, "Volume", match)
            row['volumeOz'] = match
    else:
        description_matches = re.findall(params.VOLUME_REGEX, row['description'])
        if description_matches:
            setted_list = list(set(description_matches))
            for match in setted_list:
                # Save the volume in option
                save_in_specs(row, "Volume", match)
                row['volumeOz'] = match

    return row

# Function to extract the number of plies
def extract_number_of_plies(row):
    # Extract number of plies from title
    title_match = re.search(params.PLY_REGEX, row['title'], flags=re.IGNORECASE)
    if title_match:
        # Extract the number of plies
        ply = title_match.group(0).lower()

        # Save the number of plies in option
        row['ply'] = ply
    else:
        description_match = re.search(params.PLY_REGEX, row['description'])
        if description_match:
            # Extract the number of plies
            ply = description_match.group(0).lower()

            # Save the number of plies in option
            row['ply'] = ply

    return row

# Function to check if a name is in options
def is_in_options(row, name):
    i = 0
    while (f"option.{i}.name" in row.index):
        if (row[f"option.{i}.name"] == name):
            return True
        i += 1
    return False

# Function to extract the number of rolls
def extract_number_of_rolls(row):
    if (is_in_options(row, "ROLLS") or is_in_options(row, "ROLL")):
        row['numberOfRolls'] = row['packSize']
    return row

# Function to create regex pattern
def create_regex_pattern(keywords):
    pattern = r"\b(" + "|".join(keywords).replace(" ", "\\s*") + r")\b"
    return pattern

# Function to save in product value
def save_in_product_value(row, value):
    i = 0
    saved = False
    while not saved:
        if (f"productValue.{i}" in row.index):
            if (row[f"productValue.{i}"] == ""):
                row[f"productValue.{i}"] = value
                saved = True
        else:
            row[f"productValue.{i}"] = value
            saved = True
        i += 1

# Function to extract the product value
def extract_product_value(row):
    pattern = create_regex_pattern(params.PRODUCT_VALUE_KEYWORDS)
    matches = re.findall(pattern, row['description'], flags=re.IGNORECASE)
    if matches:
        processed_matches = [match.lower() for match in matches]
        processed_matches = list(set(processed_matches))
        processed_matches = [match.capitalize() for match in processed_matches]
        for match in processed_matches:
            save_in_product_value(row, match)
    return row

def images_to_new_format(row):
    """Function to convert the images to the new format"""
    n = 0
    images = []
    while True:
        if f"images.{n}" in row.index:
            if row[f"images.{n}"] != "":
                images.append(row[f"images.{n}"])
                n += 1

            else:
                break
        else:
            break
    return images

def specs_to_new_format(row):
    """Function to convert the specs to the new format"""
    n = 0
    specs = []
    while True:
        if f"specs.{n}.name" in row.index:
            if row[f"specs.{n}.name"] != "":
                specs.append((
                    row[f"specs.{n}.name"],
                    row[f"specs.{n}.value"]
                ))
                n += 1

            else:
                break
        else:
            break
    return specs

def options_to_new_format(row):
    """Function to convert the options to the new format"""
    n = 0
    options = []
    while True:
        if f"option.{n}.name" in row.index:
            if row[f"option.{n}.name"] != "":
                options.append((
                    row[f"option.{n}.name"],
                    row[f"option.{n}.value"]
                ))
                n += 1

            else:
                break
        else:
            break
    return options

def product_values_new_format(row):
    """Function to convert the product values to the new format"""
    n = 0
    product_values = []
    while True:
        if f"productValue.{n}" in row.index:
            if row[f"productValue.{n}"] != "":
                product_values.append(row[f"productValue.{n}"])
                n += 1

            else:
                break
        else:
            break
    return product_values
