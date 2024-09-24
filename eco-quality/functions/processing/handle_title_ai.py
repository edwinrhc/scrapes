"""Import the necessary libraries"""
import json
import pandas as pd

####################### CONVERT CSV TO JSONL###############################
# Read the CSV file
tuning_data = pd.read_csv(
    'data/gcp/extract_product_names_examples.csv',
    keep_default_na=False,
    low_memory=False
    )

# Create a JSONL file
with open('data/gcp/extract_product_names_examples.jsonl', mode='w', encoding='utf-8') as file:
    for index, row in tuning_data.iterrows():
        json.dump(row.to_dict(), file)
        file.write('\n')
###########################################################################

#########################  ###############################

###########################################################################
