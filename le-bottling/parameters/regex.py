"""Here we save the regexs patterns"""
import re

# Regex to extract units per case
UNITS_PER_CASE_RE = re.compile(r"(?i)\d+\s*Units per Case")

# Regex to extract the units perpack
UNITS_PER_PACK_RE = re.compile(r"\d+/\d+(?!\d|\.\d*OZ)")
CT_BOX_PACK_SIZE_RE = re.compile(r"(\d+)\s*CT BOX")
FILTERS_PACK_SIZE_RE = re.compile(r"FLTERS\s+(\d+)")
ONLY_CT_RE = re.compile(r"(\d+(\.\d+)?)\s*CT")
OTHER_PACK_SIZE_RE = re.compile(r"((CS|SLV|K CUP|BG)\s?)(\d+(\.\d+)?)\s")


# Regex to extract the volume
VOLUME_RE = re.compile(r"(?i)(\d+(\.\d+)?)\s*(oz|ounce|ounces|lt|ml|gal|galon|l\b)")

# Regex to extract what is between parenthesis
PARENTHESIS_RE = re.compile(r"\([^)]*\)")

# Regex to extract the capacity of the product
CAPACITY_RE = re.compile(r"(\d*\.?\d+)\s?(lb|g|kg|grs)\b", re.IGNORECASE)

# Regex to extract the format acronyms
ACRONYM_RE = re.compile(r"\bPL\b|\bCN\b|\bPK\b|PL PK|CT BOX|\bBIB\b|\bCT\b|\bBAG\b|\bNR\b|\bWM\b", re.IGNORECASE)

# Regex to clean the title
EXTRA_NUMBERS_RE = re.compile(r"(\d+(\.\d+)?)\s?([\/\-])\s")

# Refex to extract the size
SIZE_RE = re.compile(r"((STRW|STICK)\s?)(\d+(\.\d+)?)(\s|IN)?")
