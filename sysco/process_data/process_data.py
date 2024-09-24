import pandas as pd
import re
from time import time

import data_parameters as params
import processing_functions.utils as utils

timer = time()
# ON for all data
df = pd.read_csv("merged_final.csv", keep_default_na=False, dtype='str')
output_file_path = "merged_final_processed_v3.csv"

# ON for test data
# df = pd.read_csv("test_csv.csv", keep_default_na=False, dtype='str')
# output_file_path = "test_csv_processed.csv"

# Fix column names
df = df.rename(columns={'feerPerRoll': 'feetPerRoll'})
df = df.rename(columns={'numerOfSheets': 'numberOfSheets'})

# Set max productValue fields
for i in range(len(params.PRODUCT_VALUE_KEYWORDS)):
        df[f'productValue.{i}'] = ''
# Get fields
# Dimensions
# Get dimensions from title or description
df['dims_col'] = df.apply(lambda row: utils.get_match_from_text(row['description'],params.PRODUCT_DIMENSION_REGEX), axis=1)

for index, row in df.iterrows(): # Look in title if not in description
    if pd.isnull(row['dims_col']) or row['dims_col'] == '':
        df.at[index,'dims_col'] = utils.extract_dimensions_from_title(row['title'])

# Dimensions to dict
df['dims_col'] = df['dims_col'].apply(utils.dimension_lwh_dict) # Dimension to dict
for fields in [('productLength','L'),('productWidth','W'),('productHeight','H')]: # Each dim to corresponding field
    df[fields[0]] = df['dims_col'].apply(lambda x: f"{x[fields[1]]} {x['unit']}" if x and x[fields[1]] else '')

df = df.drop(columns=['dims_col'])

# Others
# From description
df['volume'] = df.apply(lambda row: utils.get_match_from_text(row['description'],params.VOLUME_REGEX), axis=1)
df['caseSize'] = df.apply(lambda row: utils.get_match_from_text(row['description'],params.CASE_REGEX), axis=1)
df['color'] = df.apply(lambda row: utils.get_attr_from_text(row['description'],params.COLOR_KEYWORDS), axis=1)
df['feetPerRoll'] = df.apply(lambda row: utils.get_match_from_text(row['description'],params.FEET_PER_ROLL_REGEX), axis=1)
df['numberOfSheets'] = df.apply(lambda row: utils.get_match_from_text(row['description'],params.SHEET_PER_ROLL_REGEX), axis=1)

## From title if not in descrption
df['ply'] = df.apply(lambda row: utils.get_match_from_text(row['title'],params.PLY_REGEX), axis=1) # description has mixed ply info

for col in ['volume', 'caseSize', 'color']:
    for index, row in df.iterrows():
        if pd.isnull(row[col]) or row[col] == '':
            match col:
                case 'color':
                    df.at[index,col] = utils.get_attr_from_text(row['title'], params.COLOR_KEYWORDS)
                case 'volume':
                    df.at[index,col] = utils.get_match_from_text(row['title'], params.VOLUME_REGEX)
                case 'caseSize':
                    df.at[index,col] = utils.get_match_from_text(row['title'], params.CASE_REGEX)

## Sysco Specifics
df['stdSize'] = df.apply(lambda row: utils.get_match_from_text(row['syscoPackSize'].replace('1/', ''),params.STD_SIZE_REGEX), axis=1)
# Assigning the values to 'caseSize' column where it is empty
split_values = df['syscoPackSize'].str.split('/').str[0]
df.loc[df['caseSize'] == '', 'caseSize'] = split_values[df['caseSize'] == '']

# Standardize fields
df['volume'] = df['volume'].apply(utils.standardize_volume)
df['caseSize'] = df['caseSize'].apply(utils.extract_num_from_text)
df['color'] = df['color'].apply(lambda row: utils.standardize_attr(row, params.COLOR_FORMATS))
df['ply'] = df['ply'].apply(utils.extract_num_from_text)
df['packageLength'] = df['packageLength'].str.lower()
df['packageWidth'] = df['packageWidth'].str.lower()
df['packageHeight'] = df['packageHeight'].str.lower()
df['feetPerRoll'] = df['feetPerRoll'].str.replace(',', '').apply(utils.extract_num_from_text)
df['numberOfSheets'] = df['numberOfSheets'].str.replace(',', '').apply(utils.extract_num_from_text)
df['stdSize'] = df['stdSize'].apply(lambda row: utils.standardize_attr(row, params.STD_SIZE_FORMATTING))
df['brand'] = df['brand'].apply(lambda x: re.sub(r'&amp;', '&', x))

# Set options
# Apply the processing to each row
for index, row in df.iterrows():
    df.at[index,'productWeight'] = utils.from_specs(row, "Net Weight per Case") # Product weight from specs
    # Fields to options
    if row['color']:
        df.iloc[index] = utils.save_in_option(row, 'Color', row['color'])
    if row['caseSize']:
        df.iloc[index] = utils.save_in_option(row, 'Case of', row['caseSize'])

    # Set product values
    df.iloc[index] = utils.set_product_value(df, row, params.PRODUCT_VALUE_KEYWORDS)


## AvailableForSale = False if fields are empty
not_available_empty_fields = ['price','title','images.0']
for field in not_available_empty_fields:
    df.loc[df[field] == '', 'availableForSale'] = 'False'

## General
df['canCustomize'] = 'False'
        
# Clean title
regex_list = [
    params.CASE_REGEX,
    params.SIZE_REGEX_1,
    params.SIZE_REGEX_2,
    params.VOLUME_REGEX,
    params.PRODUCT_DIMENSION_REGEX,
    params.PLY_REGEX,
    params.WEIGHT_REGEX,
]

key_words =[
    params.COLOR_KEYWORDS,
    params.RANDOM_TITLE_WORDS,
]

df['title'] = df['title'].apply(lambda row: utils.clean_title(row,regex_list=regex_list, key_words=key_words))

# Clean df
df = df.drop(columns=['volumeOZ'])
df = df.drop(columns=['volumeML'])
df = df.drop(columns=['syscoPackSize'])
df = df.drop(columns=['syscoId'])
# Save DataFrame to csv
df.to_csv(output_file_path ,index=False)

print(f'Time elapsed: {(time() - timer)/60} minutes')
  