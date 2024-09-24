import pandas as pd



df = pd.read_csv("./process_data/merged_final.csv", keep_default_na=False, dtype='str')

print(df[['syscoId', 'caseSize', 'syscoPackSize']].head())

split_values = df['syscoPackSize'].str.split('/').str[0]
df.loc[df['caseSize'] == '', 'caseSize'] = split_values[df['caseSize'] == '']



print(df[['syscoId', 'caseSize', 'syscoPackSize']].head())