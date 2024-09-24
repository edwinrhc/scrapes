import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from dzeeusa import params
import re
import time

# PRODUCTO bathroom_Amenities

# Regex para capturar volumen y unidades
volume_pattern = re.compile(r'(\d+)\s*(ml|grams|L|ML|Grams)', re.IGNORECASE)

# Regex para identificar tipos de dispensación
dispensing_types_patterns = {
    'Pump': re.compile(r'\bpump\b', re.IGNORECASE),
    'Spray': re.compile(r'\bspray\b', re.IGNORECASE),
    'Squeeze': re.compile(r'\bsqueeze\b', re.IGNORECASE),
}

########################################################################################
# Inicio Ayuda
# Función para obtener el tamaño del paquete
def get_packSize(product_name):
    product_name_lower = product_name.lower()
    pack_sizes = {
        'dozen': 'Dozen',
        'dz': 'Dozen',
        'doz': 'Dozen',
        'each': '1',
        'Each': '1',
        'item': '1',
        'Item': '1',
        'pcs': '1'
    }
    for key, value in pack_sizes.items():
        if key in product_name_lower:
            return value
    return None

def get_setPack_value(text):
    # Definimos una expresión regular para encontrar el número seguido de "Pcs"
    match = re.search(r'\b([1-9][0-9]{0,3})\s*pcs\b', text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def get_casePack_value(text):
    matches = re.findall(r'\b(\d+)\s*(Pcs|Pcs/Cs|Pcs/Case|Pieces/Case|Pieces|case|/Case|dz|Cans/Case)', text, re.IGNORECASE)
    total_pcs = sum(int(match[0]) for match in matches)
    return total_pcs




def get_volume(product_name):
    match = volume_pattern.search(product_name)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return None
########################################################################################

def get_dispensing_type(product_name):
    for type_name, pattern in dispensing_types_patterns.items():
        if pattern.search(product_name):
            return type_name
    return None

########################################################################################
def get_packaging_type(product_name):

    if any(x in product_name.lower() for x in ['bottle', 'bottles']):
        return 'Bottle'
    if 'tube' in product_name.lower():
        return 'Tube'
    return None

########################################################################################
def get_stdSize_type(product_name):
    if 'full' in product_name.lower():
        return 'Full'
    if 'twin' in product_name.lower():
        return 'Twin'
    if  'king' in product_name.lower():
        return 'King'
    if 'queen' in product_name.lower():
        return 'Queen'
    return None

##############################################################################
def get_gsm_value(text):
    #Definimos una expresión regular
    match = re.search(r'\b([1-9][0-9]{0,3})\s*GSM\b', text)
    if match:
        return match.group(1)+" GSM"
    return None
########################################################################################

def get_caseSize_value(product_name):
    # Busca un número seguido directamente por 'Pcs'
    match = re.search(r'\b(\d+)\s*(Pcs|Pack|Pcs/Cs|Pcs/case|Pieces/Case)', product_name, re.IGNORECASE)
    if match:
        return match.group(1)
    return None
def sum_case_sizes(text):
    matches = re.findall(r'\b(\d+)\s*(Pcs|Pack|Pcs/Cs|Pcs/Case|Pieces/Case|Pcs/Set|Pieces|case)', text, re.IGNORECASE)
    total_pcs = sum(int(match[0]) for match in matches)
    return total_pcs

def get_box_value(product_name):
    match = re.search(r'\b(\d+)\s*(box|Box)',product_name,re.IGNORECASE)
    if match:
        return match.group(1)
    return None