import pandas as pd

BASE_CSV_PATH = r'C:/Users/smass/Desktop/csv - Copy/'

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

for sub_cat in SUPPLIES_SUBCATEGORIES:
    
    category_name = 'suppliesequipment'
    sub_category_name = sub_cat
    
    file_path = BASE_CSV_PATH + category_name + '_' + sub_category_name + '_full.csv'
        
    df = pd.read_csv(file_path, encoding='utf-8', dtype='str')

    df['vendorCategory.0'] = categories_dict[category_name]
    df['vendorCategory.1'] = sub_category_dict[sub_category_name]


    df.to_csv(file_path, index=False, encoding='utf-8')