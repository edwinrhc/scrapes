import pandas as pd


output_file_path = "merged_final.csv"
# Load DataFrame
file_path = 'merged_missing.csv'
df = pd.read_csv(file_path, keep_default_na=False, dtype='str')
# Function to identify the row with more non-empty fields
def keep_more_non_empty(group):
    max_non_empty_row = group.iloc[0]
    max_non_empty_count = sum(1 for value in max_non_empty_row if value != '')

    for index, row in group.iterrows():
        non_empty_count = sum(1 for value in row if value != '')
        if non_empty_count > max_non_empty_count:
            max_non_empty_row = row
            max_non_empty_count = non_empty_count

    return max_non_empty_row

# Group by 'syscoId' and apply the function to keep the row with more non-empty fields
df_cleaned = df.groupby('syscoId').apply(keep_more_non_empty).reset_index(drop=True)

df_cleaned.to_csv(output_file_path, index=False)
