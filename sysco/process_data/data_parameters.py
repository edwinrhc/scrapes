COLOR_KEYWORDS = [
    "Ashwood",
    "Dark","drk","dk",
    "Granite","Grnt",
    "Graphite",
    "Light",
    "Navy",
    "Matte",
    "Steel",
    "Slate","slt","slt bl"
    "Onyx",
    "Amber","Ambr",
    "Antique Parchment","Ant Par",
    "Bamboo",
    "Beige",
    "Black","blk",
    "Blue",
    "Bold Mint",
    "Brown",
    "Burgundy",
    "Chicago",
    "Coal",
    "Cranberry",
    "Dark Wood",
    "Gingham",
    "Gray","gry",
    "Green",
    "Grey",
    "Ivory",
    "Jade",
    "Latte",
    "Mahogany",
    "Manhattan",
    "Onyx"
    "Orange",
    "Pink",
    "Red",
    "Sedona",
    "Smooth Mint",
    "Sunday",
    "White",
    "Yellow",
]

COLOR_FORMATS={
    "ambr":"Amber",
    "ant par":"Antique Parchment",
    "black steel":"Steel Black",
    "mint smooth":"Smooth Mint",
    "carmel":"Caramel",
    "slt":"Slate",
    "slt bl":"Slate Black",
    "drk":"Dark",
    "gry":"Gray",
    "blk":"Black",
}


CASE_FORMAT_EXAMPLES = [
    
    "80pc",
    "80 pc",
    "150pieces",
    "173 pieces",
    
    'case Of 12',
    'box of 200',
    
    "units per case:1",
    "units per case: 1",

    "contain 1",
    "contain 150",
    "contains 1",
    "contains 150",

    "quantity of inner pack1",
    "quantity of inner pack 1",    
    "quantity of inner pack:1",
    "quantity of inner pack: 1",
    
    "yields 2.5 pumps per case",
    "yields 24 products per case",
    "yields 245 kljsdf per case",
    
]

CASE_REGEX = r"\b(?:\d+\s*(?:pc|pieces)|(?:units|contain(?:s)?|quantity of inner pack|yields)\s+(?:per\s+case\s*:\s*)?\d+|quantity of inner pack\s*(?::?\s*)?\d+|case\s+of\s+\d+|box\s+of\s+\d+)\b"

SIZE_FORMATS_EXAMPLES_1 = [
    "6\"",
    "6\" in",
    "7\" inch",
    "8\" inches",
    
    "6\"l", # 6 inches long
    
    "20-7/8\"",
    "6-7/8\" in",
    "10-7/8\" inch",
    "20-2/8\" inches",
    
    "2.5\"",
    "3.5\" in",
    "3.5\" inch",
    "6.5\" inches",

    "7\" x 10\" ",
    "8\" x 11\" in",
    "6\" x 15\" inch",
    "2\" x 12\" inches",

    "7.5\" x 10.5\" ",
    "8.5\" x 30.5\" in",
    "5.5\" x 8.5\" inch",
    "2.5\" x 1.5\" inches",

    "7\" x 10.5\" ",
    "7\" x 10.5\" in",
    "7\" x 10.5\" inch",
    "7\" x 10.5\" inches",

    "7.5\" x 10\" ",
    "7.5\" x 10\" in",
    "7.5\" x 10\" inch",
    "7.5\" x 10\" inches",

    "7\"x 10\" ",
    "7\"x 10\" in",
    "7\"x 10\" inch",
    "7\"x 10\" inches",

    "7.5\"x 10.5\" ",
    "7.5\"x 10.5\" in",
    "7.5\"x 10.5\" inch",
    "7.5\"x 10.5\" inches",
    
    "7\"x 10.5\" ",
    "7\"x 10.5\" in",
    "7\"x 10.5\" inch",
    "7\"x 10.5\" inches",

    "7.5\"x 10\" ",
    "7.5\"x 10\" in",
    "7.5\"x 10\" inch",
    "7.5\"x 10\" inches",
  
    "7.5\" x 10\" x 2\" ",
    "7.5\" x 10\" x 2\" in",
    "7.5\" x 10\" x 2\" inch",
    "7.5\" x 10\" x 2\" inches",
    
    "7.5\"x 10\" x 2\" ",
    "7.5\"x 10\" x 2\" in",
    "7.5\"x 10\" x 2\" inch",
    "7.5\"x 10\" x 2\" inches",

    "7.5\"x 10\"x 2\" ",
    "7.5\"x 10\"x 2\" in",
    "7.5\"x 10\"x 2\" inch",
    "7.5\"x 10\"x 2\" inches",
    
    "10\" diameter",
    "10.125\" diameter",
    "6\"diameter",
    "10.125\" dia",
]

SIZE_REGEX_1 = r"\d+(?:[\d-]?\d)?(?:\/\d+)?(?:\.\d+)?\"(?:[ ]*x[ ]*\d+(?:[\d-]?\d)?(?:\/\d+)?(?:\.\d+)?\")*[ ]*(?:inch(?:es)?|in)?(?:[ ]*(diameter|dia))?[ ]*"

SIZE_FORMATS_EXAMPLES_2 = [
    
    "38in",
    "38.5inch",
    
    "38 in",
    "38.5 inch",
    
    "38in x 60in",
    "38inch x 60inch",
    
    "38.5in x 60.2in",
    "38.5inch x 60.2inch",
    
    "38.5 in x 60.2 in",
    "38.5 inch x 60.2 inch",
    
    "10in X 10in X 1.875in",
    "10inch X 10inch X 1.875inch",
    "10inches X 10inches X 1.875inches",
    
    "10 in X 10 in X 1.875 in",
    "10 inch X 10 inch X 1.875 inch",
    "10 inches X 10 inches X 1.875 inches",
]

SIZE_REGEX_2 = r"\d+\s*(?:\.\d+)?(?:\s*inch(?:es)?|in)(?:\s*x\s*\d+\s*(?:\.\d+)?(?:\s*inch(?:es)?|in)?)*"

VOLUME_FORMAT_EXAMPLES = [
    "2l",
    "3l",
    "4liter",
    "5liters",
    
    "1.9l",
    "2.3l",
    "3.1liter",
    "4.5liters",
    
    "1 l"
    "3 liter",
    "2 liters",
    
    "1.9 l"
    "3.5 liter",
    "2.4 liters",
    
    "10oz",
    "7ounce",
    "5ounces",
    
    "10.5oz",
    "7.2ounce",
    "5.3ounces",
    
    "10 oz",
    "7 ounce",
    "5 ounces",
    
    "10.5 oz",
    "7.2 ounce",
    "5.3 ounces",
    
    "2qt",
    "3quart",
    "4quarts",
    
    "2.2qt",
    "3.5quart",
    "4.6quarts",
    
    "2 qt",
    "3 quart",
    "4 quarts",
    
    "2.2 qt",
    "3.5 quart",
    "4.6 quarts",
    
    "3gal",
    "3gallon",
    "3gallons",
    
    "3.1gal",
    "3.3gallon",
    "3.5gallons",

    "3 gal",
    "3 gallon",
    "3 gallons",
    
    "3.1 gal",
    "3.3 gallon",
    "3.5 gallons",
]

VOLUME_REGEX = r"\d+(\.\d+)?(?:,\d+)?\s*(l(?:iter)?s?|ounce?s?|oz|quart(?:s)?|qt|gallon(?:s)?|gal)(?!b)"

WEIGHT_FORMAR_EXAMPLES = [

    '10 pound',
    '60 pounds',
    
    
]

WEIGHT_REGEX = r"\d+\s*pounds?"

PRODUCT_DIMENSION_EXAMPLES =[
    "product dimensions 2.75 l x 2.75 w x 0.88 h",
    "product dimensions13.00 in l x 10.75in w x 22.50in h",
    "product dimensions14.00in l x 10.00in w x 27.00in h",
    "product dimensions 2.75in l x 2.75in w x 10.63in h",
    "product dimensions5.13inlx5.13inwx10.38inh",
]

PRODUCT_DIMENSION_REGEX = r'product\s*dimensions?\s*(\d+\.\d+|\d+)\s*(in|cm)?\s*l\s*x\s*(\d+\.\d+|\d+)\s*(in|cm)?\s*w\s*x\s*(\d+\.\d+|\d+)\s*(in|cm)?\s*h'

PLY_KEYWORDS = [
  '1-ply',
  '2 ply',
]

# PLY_REGEX = r"\d+\s?-?\s?(?i)ply"
PLY_REGEX = r"\b([1-9]\d*)\s*-?\s*ply\b"

FEET_PER_ROLL_FORMAT = [
    '1,000 feet of tissue',
    '1000 feet of tissue',
    '9000 linear feet',
    '900 linear feet',
]

# FEET_PER_ROLL_REGEX = r'\d+(?:,\d+)*(?: linear feet per roll| linear feet(?: of tissue)?)(?: per roll)?'
FEET_PER_ROLL_REGEX = r'\d+(?:\.\d+)?(?:,\d+)*(?: linear feet per roll| linear feet(?: of tissue)?)(?: per roll)?'

SHEET_PER_ROLL = [
    'sheets per roll: 1,700',
    'sheets per roll 700',
    'rolls of 550 sheets',
    'rolls of: 1,550 sheets',
]

SHEET_PER_ROLL_REGEX = r'(?:sheets\sper\sroll\s?:?\s?([\d,]+)|rolls\sof\s([\d,]+)\ssheets)'

UNIT_REGEX_PATTERNS = {
  "inches": r"\b\d+(\.\d+)?\s*(inches|inch|\"|“|”)\b",
  "other_units": r"\b\d+(\.\d+)?\s*(cm|centimeters?|meters?|meter|m|feet|ft)\b",
}

PRODUCT_VALUE_KEYWORDS = [
    'compostable',
    'recycled fibers',
    'recyclable',
    'biodegradable',
    
]

STD_SIZE_FORMAT = [
    'x-sml',
    'sml',
    'small',
    'med',
    'medium',
    'lrg',
    'large',
    'x-lrg',
    '2x-lrg',
    'xx-lrg',
    '3x-lrg',
]

STD_SIZE_REGEX = r'\b(?:x-sml|sml|small|med|medium|lrg|large|x-lrg|2x-lrg|xx-lrg|3x-lrg)\b'

STD_SIZE_FORMATTING = {
    'x-sml':'XS',
    'sml':'S',
    'small':'S',
    'med':'M',
    'medium':'M',
    'lrg':'L',
    'large':'L',
    'x-lrg':'XL',
    '2x-lrg':'2XL',
    'xx-lrg':'2XL',
    '3x-lrg':'3XL',
}

RANDOM_TITLE_WORDS =[
    '&amp;',
    'width',
    'height',
]