import pandas as pd

HEADERS = [
    'uniqueIdentifier',
    'url',
    'availableForSale',
    'title',
    'description',
    'metaTitle',
    'metaDescription',
    'vendor',
    'manufacturerName',
    'brand',
    'model',
    'price',
    'vendorCategory.0',
    'vendorCategory.1',
    'vendorCategory.2',
    'vendorCategory.3',
    'vendorCategory.4',
    'categories.0',
    'categories.1',
    'material',
    'color',
    'approvedBy',
    'totalInventory',
    'images.0',
    'images.1',
    'images.2',
    'images.3',
    'images.4',
    'images.5',
    'images.6',
    'images.7',
    'images.8',
    'manufacturerNumber',
    'upc',
    'sku',
    'specs.0.name','specs.0.value',
    'specs.1.name','specs.1.value',
    'specs.2.name','specs.2.value',
    'specs.3.name','specs.3.value',
    'specs.4.name','specs.4.value',
    'specs.5.name','specs.5.value',
    'specs.6.name','specs.6.value',
    'specs.7.name','specs.7.value',
    'specs.8.name','specs.8.value',
    'specs.9.name','specs.9.value',
    'specs.10.name','specs.10.value',
    'specs.11.name','specs.11.value',
    'specs.12.name','specs.12.value',
    'option.0.name','option.0.value',
    'option.1.name','option.1.value',
    'option.2.name','option.2.value',
    'productMinOrderCases',
    'productMinOrderPrice',
    'caseSize',
    'packSize',
    'productLength',
    'productWidth',
    'productHeight',
    'productWeight',
    'packageLength',
    'packageWidth',
    'packageHeight',
    'packageWeight',
    'shippingFrom',
    'shippingCost',
    'freeShipping',
    'certificationsAndStandards',
    'origin',
    'productValue.0',
    'productValue.1',
    'canCustomize',
    'ourCost',
    'despensingType',
    'packagingType',
    'productForm',
    'scent',
    'volumeML',
    'volumeOZ',
    'border',
    'design',
    'shape',
    'towelType',
    'weightGSM',
    'feerPerRoll',
    'numberOfRolls',
    'numerOfSheets',
    'ply',
    'fit',
    'pattern',
    'threadCount',
    'pocketDepth',
    'ingredients',
    'itemForm',
    'microwaveSafe',
    'thickness',
    'syscoPackSize',
    'syscoId',
]

BASE_CSV_PATH = r'D:/OneDrive - Universidad Católica de Chile/Lilo/lilo-scrapers/sysco_v0/csv/'

SUPPLIES_SUBCATEGORIES =[
   "apparelanduniforms",
   "catering",
   "dispensers",
   "disposables",
   "foodstorageandwraps",
   "furniture",
   "healthandpersonalcare",
   "janitorialandcleaning",
   "kitchenandcutlery",
   "othersupplies",
   "registerandpos",
   "restaurantequipment",
   "tabletopdiningandbar",
]

categories_dict ={
    'suppliesequipment':'Supplies & Equipment',
}

sub_category_dict = {
    "apparelanduniforms":'Apparel and Uniforms',
    "catering":'Catering',
    "dispensers":'Dispensers',
    "disposables":'Disposables',
    "foodstorageandwraps":'Food Storage and Wraps',
    "furniture":'Furniture',
    "healthandpersonalcare":'Health and Personal Care',
    "janitorialandcleaning":'Janitorial and Cleaning',
    "kitchenandcutlery":'Kitchen and Cutlery',
    "othersupplies":'Other Supplies',
    "registerandpos":'Resgister and POS',
    "restaurantequipment":'Restaurant Equipment',
    "tabletopdiningandbar":'Tabletop Dining and Bar',
}

# Load the first CSV file into a DataFrame
merged_file = BASE_CSV_PATH + "merged_output.csv"

merged_df = pd.DataFrame()

for sub_cat in SUPPLIES_SUBCATEGORIES:
    category_name = 'suppliesequipment'
    sub_category_name = sub_cat
    
    file_path = BASE_CSV_PATH + category_name + '_' + sub_category_name + '_full.csv'
    df = pd.read_csv(file_path, encoding='utf-8', dtype='str')

    merged_df = pd.concat([merged_df,df])

    
merged_df.to_csv(merged_file, index=False, encoding='utf-8')