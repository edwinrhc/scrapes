"""Import the necessary libraries"""
import pandas as pd
import ast
import functions.processing as fp

# Open the products CSV
products_df = pd.read_csv('data/processed/products.csv', keep_default_na=False)

products_v2 = []
for index, row in products_df.iterrows():

    # Check if the product has image
    if row['images'] == '':
        row['availableForSale'] = False

    # Save caseSize in options
    row['options'] = ast.literal_eval(row['options'])
    if row['caseSize'] != '':
        row['options'].append((
            'Case size', row['caseSize']
        ))

    # Save packSize in options
    if row['packSize'] != '':
        row['options'].append((
            'Pack size', row['packSize']
        ))

    # Save Volume in options
    if row['volume'] != '':
        row['options'].append((
            'Volume', row['volume']
        ))

    # Save SIze in options
    if row['size'] != '':
        row['options'].append((
            'Size', row['size']
        ))

    new_row = row
    products_v2.append(new_row)

# Save products_df to a new CSV
products_df_v2 = pd.DataFrame(products_v2)
products_df_v2.to_csv('data/processed/products_v2.csv', index=False)
products_df_v2.to_excel('data/processed/products_v2.xlsx', index=False)
