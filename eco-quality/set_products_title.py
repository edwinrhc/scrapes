import pandas as pd

# Step 1: Load the CSV files into DataFrames
csv1 = pd.read_csv('ecoquality_products_v7.csv', keep_default_na=False, low_memory=False)
csv2 = pd.read_csv('data/gcp/ecoquality_titles_cleaned.csv', keep_default_na=False, low_memory=False)

# Set the title column if csv1's metaTitle matches csv2's title
titles_setted = []
titles = {}
length = len(csv1)
for index, row in csv1.iterrows():

    print(f"Processing {index}/{length}")

    if row['metaTitle'] in titles_setted:
        row['title'] = titles[row['metaTitle']]
    else:

        for index2, row2 in csv2.iterrows():
            if row['metaTitle'] == row2['title']:
                row['title'] = row2['cleanTitle']
                titles_setted.append(row['metaTitle'])
                titles[row['metaTitle']] = row2['cleanTitle']
                break

    csv1.loc[index] = row

# Save the updated DataFrame to a new CSV file
csv1.to_csv('ecoquality_products_v8.csv', index=False)
