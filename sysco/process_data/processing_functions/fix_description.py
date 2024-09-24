import pandas as pd

csv_file = 'missing_urls.csv'

df = pd.read_csv(csv_file, encoding='utf-8', dtype='str')


new_description = 'Product description is not available'  # New description value

# Iterate over DataFrame rows
for index, row in df.iterrows():
    if pd.isnull(row['description']):

        df.at[index, 'description'] = new_description
        df.at[index, 'metaDescription'] = new_description 



df.to_csv('mssing_urls_fixed.csv', index=False) 