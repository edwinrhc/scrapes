"""Import necessary libraries"""
import sys
sys.path.append('/home/hjmacaya/code/hjmacaya/python-projects/lilo/scrapers/lilo-scrapers/eco-quality')


import pandas as pd
import functions.processing.utils as ut

# 1. Read the CSV file
products_df = pd.read_csv('ecoquality_products_v8.csv', keep_default_na=False, low_memory=False)

# 2. Create a new column empty
products_df['options'] = ""

# 3. Extract options
new_data = []
for index, row in products_df.iterrows():
    new_row = ut.extract_selected_options_v2(row)
    new_data.append(new_row)

# 4. Create new df
new_products_df = pd.DataFrame(new_data)

# 5. Remove the options columns
columns_to_be_removed = [
    'option.0.name','option.0.value',
    'option.1.name','option.1.value',
    'option.2.name','option.2.value',
    'option.3.name','option.3.value',
    'option.4.name','option.4.value',
    'option.5.name','option.5.value',
    'option.6.name','option.6.value',
    'option.7.name','option.7.value',
    'option.8.name','option.8.value',
    'option.9.name','option.9.value',
    'option.10.name','option.10.value',
    'option.11.name','option.11.value',
    'option.12.name','option.12.value',
    'option.13.name','option.13.value',
    'option.14.name','option.14.value',
    'option.15.name','option.15.value',
    'option.16.name','option.16.value',
    'option.17.name','option.17.value',
    'option.18.name','option.18.value',
    'option.19.name','option.19.value',
    'option.20.name','option.20.value'
]
for col in columns_to_be_removed:
    if col in new_products_df.columns:
        new_products_df.drop(columns=col, inplace=True)

# 6. Save the new data
new_products_df.to_csv('ecoquality_products_v9.csv', index=False)
new_products_df.to_csv('ecoquality_products_v9.xlsx', index=False)

# 7. Check the new data
print(new_products_df[['options']].head(20))
