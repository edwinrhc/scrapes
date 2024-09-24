"""Import the necessary libraries"""
import re

import parameters.processing as ppx

####################### OPTIONS #########################
def is_volume_type(option_value):
    """Check if the option value is a volume type"""
    match = re.search(ppx.VOLUME_REGEX, option_value)
    if match:
        return True
    return False

def is_quantity_type(option_value):
    """Check if the option value is a quantity type"""
    option_value = option_value.lower()
    if "box" in option_value:
        return True
    if "x" not in option_value:
        match = re.search(ppx.QUANTITY_REGEX, option_value, re.IGNORECASE)
        if match:
            return True
    return False

def is_special_size(option_value):
    """Check if the option value is a special size"""
    match = re.search(ppx.SPECIAL_SIZE_REGEX, option_value)
    if match:
        return True
    return False

def is_capacity_type(option_value):
    """Check if the option value is a capacity type"""
    match_lb = re.search(ppx.CAPACITY_REGEX_LB, option_value, re.IGNORECASE)
    match_dogs = re.search(ppx.CAPACITY_REGEX_DOGS, option_value, re.IGNORECASE)
    if match_lb or match_dogs:
        return True
    return False

def is_roll_size(option_value):
    """Check if the option value is a roll size"""
    match = re.search(ppx.ROLL_SIZE_REGEX, option_value, re.IGNORECASE)
    if match:
        return True
    return False

def is_blade_size(option_value):
    """Check if the option value is a blade size"""
    for example in ppx.BLADE_SIZE_EXAMPLES:
        if example.lower() in option_value.lower():
            return True
    return False

def is_color_type(option_value):
    """Check if the option value is a color type"""
    for color in ppx.COLORS:
        if color.lower() in option_value.lower():
            return True
    return False

def is_combo_format(option_value):
    """Check if the option value is a combo format"""
    option_value = str(option_value)
    match_1 = re.search(ppx.COMBO_FORMAT_REGEX, option_value, re.IGNORECASE)
    match_2 = re.search(ppx.COMBO_FORMAT_REGEX_2, option_value, re.IGNORECASE)
    if match_1 or match_2:
        return True
    return False

def is_gallon_type(option_value):
    """Check if the option value is a gallon type"""
    if "gallon" in option_value.lower():
        return True
    if "gal" in option_value.lower():
        return True
    return False

def is_std_size_fraction(option_value):
    """Check if the option value is a standard size fraction"""
    match = re.search(ppx.STD_SIZE_FRACTION, option_value, re.IGNORECASE)
    if match:
        return True
    return False

def is_size_shape_size(option_value):
    """Check if the option value is a size shape type"""
    option_value = option_value.replace("''", '\"').replace("”", "\"").replace("“", "\"")
    match = re.search(ppx.SHAPE_SIZE_REGEX, option_value, re.IGNORECASE)
    if match:
        return True
    return False

def is_there_quantity_type(row):
    """Check if there is a quantity type in the options"""
    index = 0
    finished = False
    while not finished:

        if index > 20:
            break

        option_name = row[f"option.{index}.name"]

        if option_name == "":
            finished = True
            break

        if option_name.lower() in ppx.QUANTITY_NAMES:
            return True

        index += 1

    return False

def is_al_capacity_type(value):
    """Check if the option value is an al capacity type"""
    match = re.search(ppx.ALUMINUM_CAPACITY_REGEX, value, re.IGNORECASE)
    if match:
        return True
    return False

def is_std_size_type(value):
    """Check if the option value is a standard size type"""
    match = re.search(ppx.STD_SIZE_REGEX, value, re.IGNORECASE)
    if match:
        return True
    return False

def is_pastry_size(value):
    """Check if the option value is a pastry size"""
    match = re.search(ppx.PASTRY_SIZE_REGEX, value, re.IGNORECASE)
    if match:
        return True
    return False

def is_pepper_size(value):
    """Check if the option value is a pepper size"""

    # Initial dimension check
    if not re.search(ppx.PEPPER_SIZE_REGEX_1, value, re.IGNORECASE):
        return False  # Initial dimension not found

    # Check if it continues correctly with either diameter or "x"
    if not re.search(ppx.PEPPER_SIZE_REGEX_2, value, re.IGNORECASE):
        return False  # Neither diameter nor "x" found

    # Final check for height measurement
    if re.search(ppx.PEPPER_SIZE_REGEX_3, value, re.IGNORECASE):
        return True  # Height measurement found

    return False  # Default case if none of the above conditions are met

def is_fraction(value):
    """Check if the option value is a fraction"""
    match = re.search(ppx.FRACTION_REGEX, value)
    if match:
        return True
    return False

def format_size_option(row, name, value):
    """Format the size options of the product"""

    value = value.replace("''", '\"').replace("”", "\"").replace("“", "\"")

    # 0.1 Check if is fraction
    if is_fraction(value):
        return "Size"

    # 0.2 Check if is Combo Format
    if is_combo_format(value):
        return "Combo format"

    # 1. Check if is Diameter size
    if name.lower() == "size (dia)" or name.lower() == "size diameter":
        return "Diameter"

    # 2. Check if is volume type
    if is_volume_type(value) or "oz" in name.lower() or row['title'] in ppx.PRODUCTS_WITH_BAD_VOL_STRUCTURE:
        return "Volume"

    # 3. Check if is special size
    if is_special_size(value):
        return "Special size"

    # 4. Check if is capacity type
    if is_capacity_type(value):
        return "Capacity"

    # 5. Check if is quantity type
    if is_quantity_type(value) and not is_dimension_type(value) and not is_std_size_fraction(value) and not is_size_shape_size(value) and not is_std_size_type(value):
        return "Pack size"

    # 6. Check if is Roll size
    if is_roll_size(value):
        return "Roll size"

    # 7. Check if is color
    if is_color_type(value):
        return "Color"

    # 8. Check if is std size fraction
    if is_std_size_fraction(value):
        return "Standard size"

    # 9. Check if is size shape type
    if is_size_shape_size(value):
        return "Size shape"

    return name

def fromat_all_options(row):
    """Format all the options of the product"""
    index = 0
    finished = False
    while not finished:
        if index > 20:
            break

        option_name = row[f"option.{index}.name"]
        option_value = row[f"option.{index}.value"]

        if option_name == "":
            finished = True
            break

        if option_name == "Size (inch)" or option_name == "Size (inches)":
            row[f"option.{index}.name"] = "Size"

        elif option_name == "Size (LB)":
            row[f"option.{index}.name"] = "Capacity"

        elif "Size" in option_name.split(" "):
            if row['title'] in ppx.PRODUCTS_WITH_BAD_SIZE_STRUCTURE:
                row[f"option.{index}.name"] = "Size"
                row[f"option.{index}.value"] = option_value.strip() + " in"
            else:
                row[f"option.{index}.name"] = format_size_option(row, option_name, option_value)

        elif option_name.lower() in ppx.QUANTITY_NAMES:
            if is_combo_format(option_value):
                row[f"option.{index}.name"] = "Combo format"
            else:
                row[f"option.{index}.name"] = "Pack size"

        if "gallon" in option_name.lower():
            row[f"option.{index}.name"] = "Gallon"
            row[f"option.{index}.value"] = option_value

        index += 1
    return row

def is_dimension_type(value):
    """Check if the option value is a dimension type"""

    # 1. Check if is triple dimension
    match = re.search(ppx.TRIPLE_DIMENSION_REGEX, value, re.IGNORECASE)
    if match:
        return True

    # 2. Check if is double dimension
    match = re.search(ppx.DOUBLE_DIMENSION_REGEX, value, re.IGNORECASE)
    if match:
        return True

    # 3. Check if is single dimension
    match = re.search(ppx.SINGLE_DIMENSION_REGEX, value, re.IGNORECASE)
    if match:
        return True

    return False

def get_dimension(value):
    """Get the dimension of the product"""
    # 1. Check if is triple dimension
    match = re.search(ppx.TRIPLE_DIMENSION_REGEX, value, re.IGNORECASE)
    if match:
        return match

    # 2. Check if is double dimension
    match = re.search(ppx.DOUBLE_DIMENSION_REGEX, value, re.IGNORECASE)
    if match:
        return match

    # 3. Check if is single dimension
    match = re.search(ppx.SINGLE_DIMENSION_REGEX, value, re.IGNORECASE)
    if match:
        return match

    return None

def get_l_w_h(value):
    """Set the length, width and height of the product"""
    match = get_dimension(value)
    length, width, height = None, None, None
    if match:
        match_group = match.group()
        match_group = match_group.replace(" ", "")
        match_group = match_group.split("x")
        length = match_group[0]
        width = match_group[1] if len(match_group) > 1 else None
        height = match_group[2] if len(match_group) > 2 else None
    return length, width, height

def set_format_to_size(row):
    """Set the format to the size of the product"""
    index = 0
    finished = False
    while not finished:

        if index > 20:
            break

        option_name = row[f"option.{index}.name"]
        option_value = row[f"option.{index}.value"]

        if option_name == "":
            finished = True

        if option_name == "Size" and is_dimension_type(option_value):
            L, W, H = get_l_w_h(option_value)
            row["productLength"] = L if L else ""
            row["productWidth"] = W if W else ""
            row["productHeight"] = H if H else ""

        index += 1

    return row

def get_available_options(row):
    """Get all the available options"""
    available_options = []
    index = 0
    finished = False
    while not finished:

        if index > 20:
            break

        option_name = row[f"option.{index}.name"]

        if option_name == "":
            finished = True

        if option_name != "" and option_name not in available_options:
            available_options.append(option_name)

        index += 1

    return available_options

def get_available_options_v2(row):
    """Get all the available options"""
    available_options = {}
    index = 0
    finished = False
    while not finished:

        if index > 20:
            break

        option_name = row[f"option.{index}.name"]
        option_value = row[f"option.{index}.value"]

        if option_name == "":
            break

        if option_name != "" and option_name not in available_options:
            available_options[option_name] = []
        available_options[option_name].append(option_value)
        index += 1
    return available_options

def get_selected_options(row):
    """Get the selected options of the product"""
    selected_options = row['selectedOptions']
    if row['title'] in ppx.PRODUCTS_WITH_DEPTH:
        return [selected_options]
    elif row['title'] in ppx.PRODUCTS_WITH_ONLY_FRACTION:
        selected_options = selected_options.rsplit('/', 1)
    elif is_roll_size(selected_options):
        selected_options = selected_options.rsplit('/', 1)
    elif is_blade_size(selected_options):
        selected_options = selected_options.rsplit('/', 1)
    elif is_std_size_fraction(selected_options):
        selected_options = selected_options.rsplit('/', 1)
    elif is_al_capacity_type(selected_options):
        selected_options = selected_options.rsplit('/', 1)
    elif is_pastry_size(selected_options):
        selected_options = selected_options.rsplit('/', 1)
    elif row['title'] in ppx.PRODUCTS_WITH_BAD_STYLE_STRUCTURE:
        return [selected_options]
    elif is_pepper_size(selected_options):
        selected_options = selected_options.rsplit('/', 1)
    else:
        selected_options = selected_options.split('/')
    return selected_options

#################### STANDARDIZE #######################

def save_in_specs(row, name, value):
    """Save the name and value in the specs attribute of the product"""
    i = 0
    specs_saved = False
    while not specs_saved:

        if i > 12:
            specs_saved = True
            break

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

def standarize_volume_option(value):
    """Standarize the volume option's values"""
    match = re.search(ppx.VOLUME_REGEX, value)
    if match:
        return match.group()
    if "ounces" in value.lower():
        return value.replace("ounces", "oz")
    return value.strip() + "oz"

def standarize_size_option(value):
    """Standarize the size option's values"""
    # Set mesurement unit
    mesure_unit = "in"
    if "ft" in value.lower() or "foot" in value.lower():
        mesure_unit = "ft"

    if value.lower() in ppx.STD_SIZES:
        return value

    match_two_types = re.search(ppx.TWO_TYPE_SIZES_REGEX, value, re.IGNORECASE)
    if match_two_types:
        value = value.split("-")[0]
        new_value = value.replace(" ", "")
        return new_value.lower() + f" {mesure_unit}"

    match_pastry_size = re.search(ppx.PASTRY_SIZE_REGEX, value, re.IGNORECASE)
    if match_pastry_size:
        value = value.replace("''", '\"').replace("”", "\"").replace("“", "\"")
        return value + f" {mesure_unit}"

    if is_pepper_size(value):
        return value

    if is_fraction(value):
        return value

    l, w, h = get_l_w_h(value)
    if l and w and h:
        new_value = f"{l}x{w}x{h}"
    elif l and w:
        new_value = f"{l}x{w}"
    else:
        new_value = f"{l}"

    new_value = new_value.replace(" ", "")
    new_value = new_value.replace("\"", "")
    new_value = re.sub(ppx.MEASUREMENT_REGEX, '', new_value, flags=re.IGNORECASE)
    new_value = new_value + f" {mesure_unit}"

    return new_value.lower()

def standarize_pack_option(value):
    """Standarize the pack option's value"""
    value = str(value)
    # Check rolls
    is_roll = False
    match = re.search(ppx.GET_ROLLS_REGEX, value, re.IGNORECASE)
    if match:
        is_roll = True

    # Check pcs
    match = re.search(ppx.GET_NUMBER_REGEX, value, re.IGNORECASE)
    if match:
        pack_number = match[0]
        if is_roll:
            new_value = f"{pack_number} rolls"
        else:
            new_value = f"{pack_number} pcs"
        return new_value
    return value

def standarize_special_size_option(row, index):
    """Standarize the special size option's value"""
    option_value = row[f"option.{index}.value"]
    option_value = option_value.split("-")
    volume = option_value[0]
    size = option_value[1]
    row[f"option.{index}.name"] = "Size"
    row[f"option.{index}.value"] = size
    save_in_specs(row, "Volume", volume)

def standarize_diameter_option(value):
    """Standarize the diameter option's value"""
    match = re.search(ppx.GET_NUMBER_REGEX, value)
    if match:
        diameter = match[0]
        new_value = f"{diameter} in"
        return new_value
    return value

def standarize_capacity_option(value):
    """Standarize the capacity option's value"""
    match_al_lb = re.search(ppx.ALUMINUM_CAPACITY_REGEX, value, re.IGNORECASE)
    if match_al_lb:
        return value

    match_lb = re.search(ppx.CAPACITY_REGEX_LB, value, re.IGNORECASE)
    if match_lb:
        match_group = match_lb.group()
        capacity = match_group[0]
        new_value = f"{capacity} LB"
        return new_value

    match_dogs = re.search(ppx.CAPACITY_REGEX_DOGS, value, re.IGNORECASE)
    if match_dogs:
        match_group = match_dogs.group()
        capacity = match_group[0]
        new_value = f"{capacity} Dogs"
        return new_value
    return value

def standarize_single_dimension(value):
    """Standarize the single dimension option's value"""
    match = re.search(ppx.GET_NUMBER_REGEX, value, re.IGNORECASE)
    if match:
        new_value = match.group()
        new_value = f"{new_value} in"
        return new_value
    return value

def standarize_combo_format(value):
    """Standarize the combo format option's value"""
    match = re.search(ppx.COMBO_FORMAT_REGEX, value, re.IGNORECASE)
    if match:
        # Extract the matched values
        x_value, _, y_value, w_value, _, z_value = match.groups()[0], match.groups()[1], match.groups()[3], match.groups()[5], match.groups()[6], match.groups()[8]

        # Format the values ensuring X and W are formatted as floats or integers appropriately, and Y and Z as integers
        formatted_string = f"{float(x_value) if '.' in x_value else int(x_value)} in ({int(y_value)} pcs) + {float(w_value) if '.' in w_value else int(w_value)} in ({int(z_value)} pcs)"
        return formatted_string
    return value

def standarize_shape_size_option(row, index):
    """Standarize the shape size option's value"""
    row[f"option.{index}.value"] = row[f"option.{index}.value"].replace("''", '\"').replace("”", "\"").replace("“", "\"")
    match = re.search(ppx.SHAPE_SIZE_REGEX, row[f"option.{index}.value"], re.IGNORECASE)
    if match:
        length = match.group(1)
        shape = match.group(3)
        row['productLength'] = length + " in"
        row['shape'] = shape



def standarize_options_values(row):
    """Function to standarize the options values"""
    index = 0
    finished = False
    while not finished:

        if index > 20:
            break

        option_name = row[f"option.{index}.name"]
        option_value = row[f"option.{index}.value"]

        if option_name == "":
            finished = True
            break

        if option_name == "Size":
            option_value = option_value.replace("''", '\"').replace("”", "\"").replace("“", "\"")
            row[f"option.{index}.value"] = standarize_size_option(option_value)

        if option_name == "Volume":
            row[f"option.{index}.value"] = standarize_volume_option(option_value)

        if option_name == "Pack size":
            row[f"option.{index}.value"] = standarize_pack_option(option_value)

        if option_name == "Special size":
            standarize_special_size_option(row, index)

        if option_name == "Diameter":
            row[f"option.{index}.value"] = standarize_diameter_option(option_value)

        if option_name == "Capacity":
            row[f"option.{index}.value"] = standarize_capacity_option(option_value)

        if option_name == "Combo format":
            row[f"option.{index}.value"] = standarize_combo_format(option_value)

        index += 1

    return row

#################### STANDARDIZE #######################

# def extract_pepper_data(value):
#     """Extract the pepper data"""
#     # Step 1: Match the initial dimension and measurement unit
#     initial_match = re.search(pattern_initial_dimension, description, re.IGNORECASE)
#     if not initial_match:
#         return "No initial dimension found."

#     # Determine the next part of the description
#     remainder_of_description = description[initial_match.end():]

#     # Check for Diameter condition
#     if re.search(pattern_dia, remainder_of_description, re.IGNORECASE):
#         dia_match = re.search(pattern_dia, remainder_of_description, re.IGNORECASE)
#         height_match = re.search(pattern_height_measurement, remainder_of_description[dia_match.end():], re.IGNORECASE)
#         if height_match:
#             return f"Initial Dimension: {initial_match.group(0)} Diameter, Height: {height_match.group(0)}"
#         else:
#             return "Diameter mentioned but no valid height found."

#     # Check for "x" condition
#     elif re.search(pattern_x_condition, remainder_of_description, re.IGNORECASE):
#         # Find all occurrences of dimensions after "x"
#         dimensions_after_x = re.findall(pattern_initial_dimension, remainder_of_description, re.IGNORECASE)
#         height_match = re.search(pattern_height_measurement, remainder_of_description, re.IGNORECASE)
#         if dimensions_after_x and height_match:
#             dimensions_str = " x ".join([dim[0] for dim in dimensions_after_x])
#             return f"Dimensions: {initial_match.group(0)} x {dimensions_str}, Height: {height_match.group(0)}"
#         else:
#             return "'x' mentioned but no valid dimensions found."

#     else:
#         return "No valid diameter or 'x' condition found."

def get_al_data(value):
    """Get the data of the al capacity"""
    match = re.search(ppx.ALUMINUM_CAPACITY_REGEX, value, re.IGNORECASE)
    if match:
        capacity = match.group(1) + " " + match.group(2)
        shape = match.group(3)
        return capacity, shape
    return None, None

def get_shape_size(value):
    """Get the shape and size of the product"""
    value = value.replace("''", '\"').replace("”", "\"").replace("“", "\"")
    match = re.search(ppx.SHAPE_SIZE_REGEX, value, re.IGNORECASE)
    if match:
        length = match.group(1)
        shape = match.group(3)
        return length, shape
    return None, None

def re_set_options(row):
    """Re-set the options of the product"""
    index = 0
    finished = False
    while not finished:

        if index > 20:
            break

        option_name = row[f"option.{index}.name"]
        option_value = row[f"option.{index}.value"]

        if option_name == "":
            break

        if option_name == "Size shape":
            length, shape = get_shape_size(option_value)
            row[f"option.{index}.name"] = "Size"
            row[f"option.{index}.value"] = length + " in"

        if option_name == "Capacity":
            if is_al_capacity_type(option_value):
                capacity, shape = get_al_data(option_value)
                row[f"option.{index}.name"] = "Capacity"
                row[f"option.{index}.value"] = capacity

        index += 1


def save_selected_option(row, option, option_value):
    """Set and save the selected option"""

    if option == 'Size':
        if is_pepper_size(option_value):
            save_in_specs(row, option, option_value)
        elif is_pastry_size(option_value):
            row['productLength'] = option_value
        elif is_fraction(option_value):
            save_in_specs(row, option, option_value)
        else:
            length, width, height = get_l_w_h(option_value.lower())
            row['productLength'] = standarize_single_dimension(length) if length else ""
            row['productWidth'] = standarize_single_dimension(width) if width else ""
            row['productHeight'] = standarize_single_dimension(height) if height else ""

    elif option == 'Color':
        row['color'] = option_value

    elif option == 'Pack size':
        row['packSize'] = standarize_pack_option(option_value)
        row['caseSize'] = 1

    elif option == 'Capacity':
        option_value = standarize_capacity_option(option_value)
        if is_al_capacity_type(option_value):
            capacity, shape = get_al_data(option_value)
            row['shape'] = shape
            save_in_specs(row, option, capacity)
            re_set_options(row)
        else:
            save_in_specs(row, option, option_value)

    elif option == 'Depth':
        row['productHeight'] = option_value
        save_in_specs(row, option, option_value)

    # elif option == 'Special size':
    #     # Set the special size

    elif option == 'Volume':
        row['volumeOZ'] = standarize_volume_option(option_value)

    elif option == 'Style':
        save_in_specs(row, option, option_value)

    elif option == 'Roll size':
        width, length = extract_feet_per_roll(option_value)
        row['productWidth'] = width + " in"
        row['productLength'] = length + " ft"
        row['feerPerRoll'] = length + " ft"

    elif option == 'Combo format':
        combo = standarize_combo_format(option_value)
        save_in_specs(row, option, combo)

    elif option == 'Material':
        row['material'] = option_value

    elif option == 'Gallon':
        save_in_specs(row, option, option_value)

    elif option == 'Size shape':
        print(f"Extracting options for {row['title']}...")

        length, shape = get_shape_size(option_value)
        row['productLength'] = length + " in"
        row['shape'] = shape
        re_set_options(row)

    elif option == 'Stype':
        save_in_specs(row, option, option_value)

    elif option == "Wattage":
        save_in_specs(row, option, option_value)

    # Save in a new column called "options"
    row['options'].append((option, option_value))


def save_selected_option_v2(row, option, option_value, options_list):
    """Set and save the selected option"""

    if option == 'Size':
        options_list.append((option, option_value))
        if is_pepper_size(option_value):
            save_in_specs(row, option, option_value)
        elif is_pastry_size(option_value):
            row['productLength'] = option_value
        elif is_fraction(option_value):
            save_in_specs(row, option, option_value)
        else:
            length, width, height = get_l_w_h(option_value.lower())
            row['productLength'] = standarize_single_dimension(length) if length else ""
            row['productWidth'] = standarize_single_dimension(width) if width else ""
            row['productHeight'] = standarize_single_dimension(height) if height else ""

    elif option == 'Color':
        row['color'] = option_value
        options_list.append((option, option_value))


    elif option == 'Pack size':
        row['packSize'] = standarize_pack_option(option_value)
        row['caseSize'] = 1
        options_list.append((option, standarize_pack_option(option_value)))


    elif option == 'Capacity':
        option_value = standarize_capacity_option(option_value)
        options_list.append((option, option_value))
        if is_al_capacity_type(option_value):
            capacity, shape = get_al_data(option_value)
            row['shape'] = shape
            save_in_specs(row, option, capacity)
            re_set_options(row)
        else:
            save_in_specs(row, option, option_value)

    elif option == 'Depth':
        row['productHeight'] = option_value
        save_in_specs(row, option, option_value)
        options_list.append((option, option_value))

    # elif option == 'Special size':
    #     # Set the special size

    elif option == 'Volume':
        row['volumeOZ'] = standarize_volume_option(option_value)
        options_list.append((option, standarize_volume_option(option_value)))

    elif option == 'Style':
        save_in_specs(row, option, option_value)
        options_list.append((option, option_value))

    elif option == 'Roll size':
        width, length = extract_feet_per_roll(option_value)
        row['productWidth'] = width + " in"
        row['productLength'] = length + " ft"
        row['feerPerRoll'] = length + " ft"
        options_list.append((option, option_value))

    elif option == 'Combo format':
        combo = standarize_combo_format(option_value)
        save_in_specs(row, option, combo)
        options_list.append((option, standarize_combo_format(option_value)))

    elif option == 'Material':
        row['material'] = option_value
        options_list.append((option, option_value))

    elif option == 'Gallon':
        save_in_specs(row, option, option_value)
        options_list.append((option, option_value))

    elif option == 'Size shape':
        print(f"Extracting options for {row['title']}...")

        options_list.append((option, option_value))

        length, shape = get_shape_size(option_value)
        row['productLength'] = length + " in"
        row['shape'] = shape
        re_set_options(row)

    elif option == 'Stype':
        save_in_specs(row, option, option_value)
        options_list.append((option, option_value))

    elif option == "Wattage":
        save_in_specs(row, option, option_value)
        options_list.append((option, option_value))

def check_for_option_name(option_value):
    """Function to get the option name"""
    # 1. Check if is volume type
    if is_volume_type(option_value):
        return "Volume"

    # 2. Check if is roll size
    if is_roll_size(option_value):
        return "Roll size"

    # 3. Check if is special size
    if is_special_size(option_value):
        return "Special size"

    # 4. Check if is capacity type
    if is_capacity_type(option_value):
        return "Capacity"

    # 5. Check if is combo format
    if is_combo_format(option_value):
        return "Combo format"

    # 6. Check if is size
    if is_dimension_type(option_value):
        return "Size"

    # 7. Check if is quantity type
    if is_quantity_type(option_value):
        return "Pack size"

    # 8. Check if is Gallon
    if is_gallon_type(option_value):
        return "Gallon"

    # 9. Check if is material

    # 10. Check if is Standard size fraction
    if is_std_size_fraction(option_value):
        return "Standard size"

    # 8. Is color
    return "Color"


def set_new_options(selected_options):
    """Set new options when they don't match"""
    new_options = []
    for selected_option in selected_options:
        option_name = check_for_option_name(selected_option)
        if option_name:
            new_options.append(option_name)
        else:
            print(f"Option not found: {selected_option}")
    return new_options

def extract_selected_options(row):
    """Function to extract data from selected options"""

    # 1. Get all the avaible options
    available_options = get_available_options(row)

    # 2. Get the selected options
    if len(available_options) > 0:
        selected_options = get_selected_options(row)
        if len(selected_options) != len(available_options):

            print("\n")
            print(f"Porduct name: {row['title']}")
            print(f"Available options: {available_options}")
            print(f"Selected options: {selected_options}")
            print("\n")

            available_options = set_new_options(selected_options)

        for i, option in enumerate(available_options):
            save_selected_option(row, option, selected_options[i])

    return row

def extract_selected_options_v2(row):
    """Function to extract data from selected options"""

    # 1. Get all the avaible options
    available_options = get_available_options(row)

    # 2. Get the selected options
    options_list = []
    if len(available_options) > 0:
        selected_options = get_selected_options(row)
        if len(selected_options) != len(available_options):

            print("\n")
            print(f"Porduct name: {row['title']}")
            print(f"Available options: {available_options}")
            print(f"Selected options: {selected_options}")
            print("\n")

            available_options = set_new_options(selected_options)

        for i, option in enumerate(available_options):
            save_selected_option_v2(row, option, selected_options[i], options_list)

    row['options'] = options_list

    return row
####################### OPTIONS #########################

######################## VALUE ##########################
def create_regex_pattern(keywords):
    """Function to create a regex pattern"""
    pattern = r"\b(" + "|".join(keywords).replace(" ", "\\s*") + r")\b"
    return pattern

def save_in_product_value(row, value):
    """Save the value in the product value attribute of the product"""
    i = 0
    saved = False
    while not saved:
        if i == 2:
            break
        if (f"productValue.{i}" in row.index):
            if (row[f"productValue.{i}"] == ""):
                row[f"productValue.{i}"] = value
                saved = True
        else:
            row[f"productValue.{i}"] = value
            saved = True
        i += 1

def extract_product_value(row):
    """Extract the product value from the description of the product"""
    pattern = create_regex_pattern(ppx.PRODUCT_VALUE_KEYWORDS)
    matches = re.findall(pattern, row['description'], flags=re.IGNORECASE)
    if matches:
        processed_matches = [match.lower() for match in matches]
        processed_matches = list(set(processed_matches))
        processed_matches = [match.capitalize() for match in processed_matches]
        for match in processed_matches:
            save_in_product_value(row, match)
    return row
######################## VALUE ##########################

######################## ROLLS ##########################
def extract_number_of_rolls(row):
    """Extract the number of rolls"""
    pack_size = row['packSize']
    match = re.search(ppx.GET_ROLLS_REGEX, pack_size)
    if match:
        number_match = re.search(ppx.GET_NUMBER_REGEX, pack_size)
        if number_match:
            rolls = number_match[0]
            row['numberOfRolls'] = rolls
    return row

def extract_feet_per_roll(option_value):
    """Extract the feet per roll"""
    match = re.search(ppx.ROLL_SIZE_REGEX, option_value)
    if match:
        width = match[1].strip()
        length = match[2].strip()
        return width, length
    return None, None
######################## ROLLS ##########################


######################## TITLE ##########################
def extract_volume_from_title(title):
    """Extract the volume from the title"""
    volume = ""

    match_volumes = re.findall(ppx.VOLUME_REGEX, title, re.IGNORECASE)
    if match_volumes and len(match_volumes) == 1:
        volume = standarize_volume_option(match_volumes[0])
        volume = volume.replace(" ", "")
        oz_index = volume.find("oz")
        #  Add space between number and oz
        if oz_index > 0:
            volume = volume[:oz_index] + " " + volume[oz_index:]
    else:
        print(f"No volumes found in title: {title}")
    return volume
######################## TITLE ##########################

####################### DESCRIP #########################
####################### DESCRIP #########################
