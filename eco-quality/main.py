"""Import the necessary libraries"""
import glob
import os
import pandas as pd
import parameters.products as ppd

# Step 1: Get the list of all CSV files in the specified directory
# csv_files = glob.glob('data/final/*.csv')

# if os.path.exists('ecoquality_products.csv'):
#     products_df = pd.read_csv('ecoquality_products.csv', keep_default_na=False, low_memory=False)
# else:
#     products_df = pd.DataFrame(columns=ppd.HEADERS)

################# Fill missing fields #################
# # 1. Set our cost
# products_df['ourCost'] = products_df['price']

# # 2. Add manufacturer name and brand
# products_df['manufacturerName'] = 'EcoQuality'
# products_df['brand'] = 'EcoQuality'

# # 3. Add canCustomize
# products_df['canCustomize'] = False

# # 4. Fix feerPerRoll column name
# products_df.rename(columns={'feerPerRoll': 'feetPerRoll'}, inplace=True)

# # 5. Check everything
# print(products_df[['ourCost', 'manufacturerName', 'brand', 'canCustomize', 'feetPerRoll']].head(15))

# # 6. Drop duplicated rows
# products_df.drop_duplicates(inplace=True)

# # 7. Save the resulting DataFrame to a new CSV file
# products_df.to_csv('ecoquality_products_v3.csv', index=False)
#######################################################


df = pd.read_csv('ecoquality_products_v8.csv', keep_default_na=False, low_memory=False)
print(df[['title', 'metaTitle']].head(20))


################## SET THE TITLES ONLY ##################
# products_df = pd.read_csv('ecoquality_products_v3.csv', keep_default_na=False, low_memory=False)
# products_df = products_df[['title']]
# print(f"Number of products: {len(products_df)}")

# # Get the unique titles
# unique_titles = products_df['title'].unique()
# print(f"Number of unique titles: {len(unique_titles)}")

# # Create a new data frame
# new_df = pd.DataFrame(columns=['title', 'cleanTitle'])

# # Add the unique titles to the new data frame
# new_df['title'] = unique_titles

# # Save the new data frame to a new CSV file
# new_df.to_csv('data/gcp/ecoquality_titles.csv', index=False)
#########################################################


# subcategory_counts = products_df.groupby('vendorCategory.1').size()

# print(subcategory_counts)

# Print the total number of products
# print(f"Total number of products: {len(products_df)}")

# reduced_df = products_df[['title']]
# reduced_df.to_csv('ecoquality_products_reduced.csv', index=False)

# products_grouped_by_category = products_df.groupby('vendorCategory.1')
# for category, group in products_grouped_by_category:
#     number_of_products = len(group['title'].unique())
#     if number_of_products > 100:
#         ten_percent = int(number_of_products * 0.1)
#     elif number_of_products > 10 and number_of_products <= 100:
#         ten_percent = 10
#     else:
#         ten_percent = number_of_products
#     print(f"Category: {category}")
#     print(f"Number of products: {number_of_products}")
#     print(f"10% of the products: {ten_percent}")
#     print(group['title'].unique()[:ten_percent])
#     print("\n")


# Step 2: Read and concatenate all CSV files into a single DataFrame
# start = 110
# for file in csv_files[start:]:
#     df = pd.read_csv(file, low_memory=False)
#     products_df = pd.concat([products_df, df], ignore_index=True)


# df_list = [pd.read_csv(file, low_memory=False) for file in csv_files]
# concatenated_df = pd.concat(df_list, ignore_index=True)

# Step 3: Remove duplicate rows
# clean_df = concatenated_df.drop_duplicates()
# clean_df = products_df.drop_duplicates()

# # Step 4: Save the resulting DataFrame to a new CSV file
# clean_df.to_csv('ecoquality_products.csv', index=False)
# clean_df.to_excel('ecoquality_products.xlsx', index=False)
