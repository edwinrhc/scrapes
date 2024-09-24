"""Params used in the processing"""

VOLUME_REGEX = r"\b(\d+\.?\d*\s?\.?oz\.?)\b"

# QUANTITY_REGEX = r"\b(\d+)\s*(pcs|pc|ps|cups per pack|pcss|cs)?\s*(?=\s*$)"
# QUANTITY_REGEX = r"(\d+)\s*(?:pcs|pc|ps|cups per pack|pcss|cs)(?:\s*for\s*\d+\s*People)?"
QUANTITY_REGEX = r"(\d+)\s*(?:pcs|pc|ps|cups per pack|pcss|cs|box|cones \/ pack)?(?:\s*for\s*\d+\s*People)?"


SPECIAL_SIZE_REGEX = r"\b(\d+(\.\d+)?L)-([a-zA-Z]+)\b"

CAPACITY_REGEX_LB = r"\b(\d+)\s*(lb|LB|Lb|lB)\b"
CAPACITY_REGEX_DOGS = r"\b(\d+)\s*(dogs|dog)\b"
ALUMINUM_CAPACITY_REGEX = r"(\d+(?: \d+/\d+)?) ?(lb|L|lt) ?(shallow|deep)"

TWO_TYPE_SIZES_REGEX = r"\d+(\.\d+)?X\d+(\.\d+)?X\d+(\.\d+)?\s*-?\s*[A-Z]+"
STD_SIZE_FRACTION = r"(Small|Medium|Large|XLarge|XSmall|X-Large|X-Small)\s?\d+\/\d+"
STD_SIZE_REGEX = r"(Small|Medium|Large|XLarge|XSmall|X-Large|X-Small)"
SHAPE_SIZE_REGEX = r"(\d+(\.\d+)?)\" (round|square|rectangular|oval|triangle)"
PASTRY_SIZE_REGEX = r"\d+-\d+/\d+ ?(in|inch|inches|\")"

PEPPER_SIZE_REGEX_1 = r"(\d+(?:-\d+/\d+)?) ?(\"|inches|inch|in|ft)?"
PEPPER_SIZE_REGEX_2 = r"(dia|diameter|x)"
PEPPER_SIZE_REGEX_3 = r"\d+H"

SINGLE_DIMENSION_REGEX = r"(\d+(?:\.\d+)?)\s*(?:(?<=\d)(?=\"|\'$)|\"|in(?:ch(?:es)?)?\b)"
DOUBLE_DIMENSION_REGEX = r"(\d+(?:\.\d+)?)(?:\"|\s*inch(es)?)?\s*[xX]\s*(\d+(?:\.\d+)?)(?:\"|\s*inch(es)?)?"
TRIPLE_DIMENSION_REGEX = r"(\d+(?:\.\d+)?)(?:\"|\s*inch(es)?)?\s*[xX]\s*(\d+(?:\.\d+)?)(?:\"|\s*inch(es)?)?\s*[xX]\s*(\d+(?:\.\d+)?)(?:\"|\s*inch(es)?)?"

SIZE_MEASUREMENTS = ["inch", "inches", "in", "\""]
MEASUREMENT_REGEX = r"(inches|inch|in|\"|INCH)"

GET_NUMBER_REGEX = r"[-+]?\d+(\.\d+)?"
GET_ROLLS_REGEX = r"(\d+)\s*(rolls|roll|rls|rl|rls\.)"
ROLL_SIZE_REGEX = r"(\d+-\d+\/\d+)\"?\s*x\s*(\d+)\s*ft\.?"

COMBO_FORMAT_REGEX = r"(\d+(\.\d+)?)(?:\s?(in|inch|inches))?\s\((\d+)\s*(pcs|PCS)\)\s*\+\s*(\d+(\.\d+)?)(?:\s?(in|inch|inches))?\s\((\d+)\s*(pcs|PCS)\)"
COMBO_FORMAT_REGEX_2 = r"(\d+(\.\d+)?)\s*&\s*(\d+(\.\d+)?)\s*(in|inch|inches)\s*combo"

BLADE_SIZE_EXAMPLES = ['4 x-3/4 inch', '10 x 1-3/8 inch', '7-15/16 x 1-1/4 inch']

FRACTION_REGEX = r"\d+/\d+"

PRODUCTS_WITH_BAD_VOL_STRUCTURE = [
    "Disposable Clear Plastic  Dome Lids for Standard Sized PET Cup (9oz,10oz,12oz,14oz,16oz,20oz,24oz)"
]

PRODUCTS_WITH_BAD_SIZE_STRUCTURE = [
    "Round Flat Aluminum Foil Board Lids - Laminated (7inch, 8inch, 9inch)"
]

PRODUCTS_WITH_BAD_STYLE_STRUCTURE = [
    "Cart/Trolley for Street Vendor Popcorn Machine, Snow Bank Snow Cone Machine, Zephyr Cotton Candy Machine"
]

PRODUCTS_WITH_ONLY_FRACTION = [
    "Polycarbonate Drain Shelf (1/6 & 1/9 Size)"
]

PRODUCTS_WITH_DEPTH = [
    "Polycarbonate Food Pan, 1/4 Size",
    "Polycarbonate Food Pan, 1/3 Size"
]

STD_SIZES = [
    "large", "medium", "small", "x-large", "x-small", "xx-large", "xl", "l", "m", "s", "xs", "xxl",
    "xlarge", "xsmall", "xxlarge", "extra large", "extra small", "extra-large", "extra-small", "3xl",
    "2xl"
]

COLORS = [
    'black', 'blue', 'brown', 'clear', 'gold', 'green', 'grey',
    'ivory', 'orange', 'pink', 'purple', 'red', 'silver', 'white',
    'yellow', 'beige', 'bronze', 'copper', 'cream', 'multicolor',
    'natural', 'rainbow', 'rose gold', 'rose gold', 'turquoise',
    'wood', 'assorted', 'metallic', 'neon', 'pastel', 'pearl',
    'transparent', 'aqua', 'burgundy', 'charcoal', 'coral',
    'black&gold', 'pink&gold', 'blue&gold', 'green&gold', 'black leaf',
    'gold leaf'
]

PRODUCT_VALUE_KEYWORDS = [
    "biodegradable", "compostable", "recycled", "eco-friendly", "sustainable", "environmentally friendly", "ecofriendly"
]

QUANTITY_NAMES = [
    "quantity",
    "pack of",
    "qnt/pack",
    "item per package",
    "items per package",
    "count/pack",
    "qty",
    "pack quantity",
    "package of",
    "packing",
    "count",
    "# of boxes",
    "serving for",
    "set of",
    "number of packs",
    "quantity/pack",
    "pack",
    "qty/pack",
    "tea bags"
    ]

DIMENSION_FORMATS_EXAMPLES = [
  "6\"",
  "6\" inch",
  "6\" inches",
  "6\" INCH",
  "6\" INCHES",
  "7\" Inch",
  "7\" Inches",

  "6.5\"",
  "6.5\" inch",
  "6.5\" inches",
  "6.5\" INCH",
  "6.5\" INCHES",
  "7.5\" Inch",
  "7.5\" Inches",

  "7\" x 10\" inch",
  "7\" x 10\" inches",
  "7\" x 10\" INCH",
  "7\" x 10\" INCHES",
  "7\" x 10\" Inch",
  "7\" x 10\" Inches",
  "7\" X 10\" inch",
  "7\" X 10\" inches",
  "7\" X 10\" INCH",
  "7\" X 10\" INCHES",
  "7\" X 10\" Inch",
  "7\" X 10\" Inches",
  "7\" x 10\"",
  "7\" X 10\"",

  "7.5\" x 10.5\" inch",
  "7.5\" x 10.5\" inches",
  "7.5\" x 10.5\" INCH",
  "7.5\" x 10.5\" INCHES",
  "7.5\" x 10.5\" Inch",
  "7.5\" x 10.5\" Inches",
  "7.5\" X 10.5\" inch",
  "7.5\" X 10.5\" inches",
  "7.5\" X 10.5\" INCH",
  "7.5\" X 10.5\" INCHES",
  "7.5\" X 10.5\" Inch",
  "7.5\" X 10.5\" Inches",
  "7.5\" x 10.5\"",
  "7.5\" X 10.5\"",

  "7\" x 10.5\" inch",
  "7\" x 10.5\" inches",
  "7\" x 10.5\" INCH",
  "7\" x 10.5\" INCHES",
  "7\" x 10.5\" Inch",
  "7\" x 10.5\" Inches",
  "7\" X 10.5\" inch",
  "7\" X 10.5\" inches",
  "7\" X 10.5\" INCH",
  "7\" X 10.5\" INCHES",
  "7\" X 10.5\" Inch",
  "7\" X 10.5\" Inches",
  "7\" x 10.5\"",
  "7\" X 10.5\"",

  "7.5\" x 10\" inch",
  "7.5\" x 10\" inches",
  "7.5\" x 10\" INCH",
  "7.5\" x 10\" INCHES",
  "7.5\" x 10\" Inch",
  "7.5\" x 10\" Inches",
  "7.5\" X 10\" inch",
  "7.5\" X 10\" inches",
  "7.5\" X 10\" INCH",
  "7.5\" X 10\" INCHES",
  "7.5\" X 10\" Inch",
  "7.5\" X 10.5\" Inches",
  "7.5\" x 10\"",
  "7.5\" X 10\"",

  "7\"x 10\" inch",
  "7\"x 10\" inches",
  "7\"x 10\" INCH",
  "7\"x 10\" INCHES",
  "7\"x 10\" Inch",
  "7\"x 10\" Inches",
  "7\"X 10\" inch",
  "7\"X 10\" inches",
  "7\"X 10\" INCH",
  "7\"X 10\" INCHES",
  "7\"X 10\" Inch",
  "7\"X 10\" Inches",
  "7\"x 10\"",
  "7\"X 10\"",

  "7.5\"x 10.5\" inch",
  "7.5\"x 10.5\" inches",
  "7.5\"x 10.5\" INCH",
  "7.5\"x 10.5\" INCHES",
  "7.5\"x 10.5\" Inch",
  "7.5\"x 10.5\" Inches",
  "7.5\"X 10.5\" inch",
  "7.5\"X 10.5\" inches",
  "7.5\"X 10.5\" INCH",
  "7.5\"X 10.5\" INCHES",
  "7.5\"X 10.5\" Inch",
  "7.5\"X 10.5\" Inches",
  "7.5\"x 10.5\"",
  "7.5\"X 10.5\"",

  "7\"x 10.5\" inch",
  "7\"x 10.5\" inches",
  "7\"x 10.5\" INCH",
  "7\"x 10.5\" INCHES",
  "7\"x 10.5\" Inch",
  "7\"x 10.5\" Inches",
  "7\"X 10.5\" inch",
  "7\"X 10.5\" inches",
  "7\"X 10.5\" INCH",
  "7\"X 10.5\" INCHES",
  "7\"X 10.5\" Inch",
  "7\"X 10.5\" Inches",
  "7\"x 10.5\"",
  "7\"X 10.5\"",

  "7.5\"x 10\" inch",
  "7.5\"x 10\" inches",
  "7.5\"x 10\" INCH",
  "7.5\"x 10\" INCHES",
  "7.5\"x 10\" Inch",
  "7.5\"x 10\" Inches",
  "7.5\"X 10\" inch",
  "7.5\"X 10\" inches",
  "7.5\"X 10\" INCH",
  "7.5\"X 10\" INCHES",
  "7.5\"X 10\" Inch",
  "7.5\"X 10.5\" Inches",
  "7.5\"x 10\"",
  "7.5\"X 10\"",

  "7\"x10\" inch",
  "7\"x10\" inches",
  "7\"x10\" INCH",
  "7\"x10\" INCHES",
  "7\"x10\" Inch",
  "7\"x10\" Inches",
  "7\"X10\" inch",
  "7\"X10\" inches",
  "7\"X10\" INCH",
  "7\"X10\" INCHES",
  "7\"X10\" Inch",
  "7\"X10\" Inches",
  "7\"x10\"",
  "7\"X10\"",

  "7.5\"x10.5\" inch",
  "7.5\"x10.5\" inches",
  "7.5\"x10.5\" INCH",
  "7.5\"x10.5\" INCHES",
  "7.5\"x10.5\" Inch",
  "7.5\"x10.5\" Inches",
  "7.5\"X10.5\" inch",
  "7.5\"X10.5\" inches",
  "7.5\"X10.5\" INCH",
  "7.5\"X10.5\" INCHES",
  "7.5\"X10.5\" Inch",
  "7.5\"X10.5\" Inches",
  "7.5\"x10.5\"",
  "7.5\"X10.5\"",

  "7\"x10.5\" inch",
  "7\"x10.5\" inches",
  "7\"x10.5\" INCH",
  "7\"x10.5\" INCHES",
  "7\"x10.5\" Inch",
  "7\"x10.5\" Inches",
  "7\"X10.5\" inch",
  "7\"X10.5\" inches",
  "7\"X10.5\" INCH",
  "7\"X10.5\" INCHES",
  "7\"X10.5\" Inch",
  "7\"X10.5\" Inches",
  "7\"x10.5\"",
  "7\"X10.5\"",

  "7.5\"x10\" inch",
  "7.5\"x10\" inches",
  "7.5\"x10\" INCH",
  "7.5\"x10\" INCHES",
  "7.5\"x10\" Inch",
  "7.5\"x10\" Inches",
  "7.5\"X10\" inch",
  "7.5\"X10\" inches",
  "7.5\"X10\" INCH",
  "7.5\"X10\" INCHES",
  "7.5\"X10\" Inch",
  "7.5\"X10.5\" Inches",
  "7.5\"x10\"",
  "7.5\"X10\"",

  "7x10 inch",
  "7x10 inches",
  "7x10 INCH",
  "7x10 INCHES",
  "7x10 Inch",
  "7x10 Inches",
  "7X10 inch",
  "7X10 inches",
  "7X10 INCH",
  "7X10 INCHES",
  "7X10 Inch",
  "7X10 Inches",
  "7x10",
  "7X10",

  "7.5x10.5 inch",
  "7.5x10.5 inches",
  "7.5x10.5 INCH",
  "7.5x10.5 INCHES",
  "7.5x10.5 Inch",
  "7.5x10.5 Inches",
  "7.5X10.5 inch",
  "7.5X10.5 inches",
  "7.5X10.5 INCH",
  "7.5X10.5 INCHES",
  "7.5X10.5 Inch",
  "7.5X10.5 Inches",
  "7.5x10.5",
  "7.5X10.5",

  "7x10.5 inch",
  "7x10.5 inches",
  "7x10.5 INCH",
  "7x10.5 INCHES",
  "7x10.5 Inch",
  "7x10.5 Inches",
  "7X10.5 inch",
  "7X10.5 inches",
  "7X10.5 INCH",
  "7X10.5 INCHES",
  "7X10.5 Inch",
  "7X10.5 Inches",
  "7x10.5",
  "7X10.5",

  "7.5x10 inch",
  "7.5x10 inches",
  "7.5x10 INCH",
  "7.5x10 INCHES",
  "7.5x10 Inch",
  "7.5x10 Inches",
  "7.5X10 inch",
  "7.5X10 inches",
  "7.5X10 INCH",
  "7.5X10 INCHES",
  "7.5X10 Inch",
  "7.5X10.5 Inches",
  "7.5x10",
  "7.5X10",
]

VOLUME_FORMATS_EXAMPLES = [
  "12 oz",
  "12 OZ",
  "12 OZ.",
  "12 oz.",
  "12.oz",
  "12.OZ",
  "12oz",
  "12OZ",
  "12.5 oz",
  "12.5 OZ",
  "12.5 OZ.",
  "12.5 oz.",
  "12.5.oz",
  "12.5.OZ",
  "12.5oz",
  "12.5OZ",
  "1.0L",
  "1.5L"
]

STANDARIZED_SIZES = [
    "X-Large",
    "Large",
    "Medium",
    "Small",
    "X-Small",
    "XX-Large",
    "XL",
    "L",
    "M",
    "S",
    "XS",
    "XXL",
    "X Large",
    "X Small"
]

ROLL_PAPER_SIZE_EXAMPLES = [
    "1-3/4\" x 150 ft."
    "2-1/4\" x 50 ft"
    "3-1/8\" x 200 ft."
    "3-1/8\" x 220 ft."
    "3-1/8\" x 230 ft."
    "1-3/4 x 150 ft."
    "2-1/4 x 50 ft"
    "3-1/8 x 200 ft."
    "3-1/8 x 220 ft."
    "3-1/8 x 230 ft."
]
