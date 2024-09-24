"""Import the necessary libraries"""
import re
import parameters.regex as pre


def get_case_size(value):
    """Function to get the case size"""
    match_case_size = re.search(pre.UNITS_PER_CASE_RE, value)
    number_match = 1
    if match_case_size:
        match_case_size = match_case_size.group()
        number_match = match_case_size.split(" ")[0]
        if str(number_match) == "0":
            number_match = 1
    return number_match

def get_pack_size(value):
    """Function to get the pack size"""
    match_pack_size = re.search(pre.UNITS_PER_PACK_RE, value)
    number_match = ""
    if match_pack_size:
        match_pack_size = match_pack_size.group()
        number_match = match_pack_size.split("/")[0]
    return number_match

def get_parenthesis_pack_size(value):
    """Function to extract pack size from parenthesis"""
    match_pack_size = re.search(pre.PARENTHESIS_RE, value)
    if match_pack_size:
        match_pack_size = match_pack_size.group()
        match_pack_size = match_pack_size.replace("(", "").replace(")", "")
        try:
            return str(int(match_pack_size))
        except ValueError:
            return ""
    return ""

def get_ct_box_size(value):
    """Function to extract the pack size from a CT BOX"""
    match_pack_size = re.search(pre.CT_BOX_PACK_SIZE_RE, value)
    number = ""
    if match_pack_size:
        number = match_pack_size.groups()[0]
    return number

def get_filters_pack_size(value):
    """Function to get the filters pack size"""
    match_pack_size = re.search(pre.FILTERS_PACK_SIZE_RE, value)
    number = ""
    if match_pack_size:
        number = match_pack_size.group()
        print(f"Filters packsize: {number}")
    return number

def get_only_ct(value):
    """Function to get only the CT number"""
    match_ct = re.search(pre.ONLY_CT_RE, value)
    if match_ct:
        match_ct = match_ct.groups()
        return match_ct[0]
    return ""

def is_only_ct(value):
    """Function to check if the value is only CT"""
    match_ct = re.search(pre.ONLY_CT_RE, value)
    if match_ct:
        return True
    return False

def get_other_pack_size(value):
    """Function to get the other pack size"""
    match_pack_size = re.search(pre.OTHER_PACK_SIZE_RE, value)
    if match_pack_size:
        match_pack_size = match_pack_size.groups()
        return match_pack_size[2]
    return ""

def is_other_pack_size(value):
    """Function to check if the value is other pack size"""
    match_pack_size = re.search(pre.OTHER_PACK_SIZE_RE, value)
    if match_pack_size:
        return True
    return False

def format_volume(value):
    """Function to format the volume"""
    value = value.lower()
    measurement_unit = None
    match_vol = re.search(pre.VOLUME_RE, value)
    if match_vol:
        match_vol = match_vol.groups()
        value = match_vol[0]
        measurement_unit = match_vol[2]

    if measurement_unit:
        return f"{value} {measurement_unit}"
    return f"{value} oz"

def extract_volume(value):
    """Function to extract the volume"""
    match_vol = re.search(pre.VOLUME_RE, value)
    if match_vol:
        match_vol = match_vol.group()
        return format_volume(match_vol)
    return ""

def extract_capacity(value):
    """Function to extract the capacity"""
    match_capacity = re.search(pre.CAPACITY_RE, value)
    if match_capacity:
        match_capacity = match_capacity.groups()
        return f"{match_capacity[0]} {match_capacity[1]}"
    return ""

def extract_size(value):
    """Function to match and extract the size"""
    match_size = re.search(pre.SIZE_RE, value)
    if match_size:
        match_size = match_size.groups()
        return match_size[2]
    return ""

def remove_case_size(value):
    """Function to remove the case size"""
    return re.sub(pre.UNITS_PER_CASE_RE, "", value)

def remove_pack_size(value):
    """Function to remove the pack size"""
    return re.sub(pre.UNITS_PER_PACK_RE, "", value)

def remove_volume(value):
    """Function to remove the volume"""
    return re.sub(pre.VOLUME_RE, "", value)

def remove_capacity(value):
    """Function to remove the capacity"""
    return re.sub(pre.CAPACITY_RE, "", value)

def remove_acronyms(value):
    """Function to remove the acronyms"""
    return re.sub(pre.ACRONYM_RE, "", value)

def remove_ct_box_size(value):
    """Function to remove the CT BOX pack size"""
    return re.sub(pre.CT_BOX_PACK_SIZE_RE, "", value)

def remove_flters_pack_size(value):
    """Function to remove the filters pack size"""
    return re.sub(pre.FILTERS_PACK_SIZE_RE, "", value)

def remove_only_ct(value):
    """Function to remove the only CT"""
    return re.sub(pre.ONLY_CT_RE, "", value)

def remove_other_pack_size(value):
    """Function to remove the other pack size"""
    return re.sub(pre.OTHER_PACK_SIZE_RE, "", value)

def remove_extra_numbers(value):
    """Function to remove the extra numbers"""
    return re.sub(pre.EXTRA_NUMBERS_RE, "", value)

def remove_size(value):
    """Function to remove the size"""
    match_size = re.search(pre.SIZE_RE, value)
    if match_size:
        match_size = match_size.groups()
        size_number = match_size[2]
        if size_number:
            return value.replace(size_number, "")
    return re.sub(pre.SIZE_RE, "", value)
