"""Import the necessary libraries"""
import pandas as pd

products_df = pd.read_csv(
    "data/scraped/products/Disposable_Tableware_products.csv",
    keep_default_na=False
)

column_indices = [22, 91, 92, 93, 94, 95, 96, 97, 98, 144, 148, 149]

selected_columns = products_df.iloc[:, column_indices]
print(selected_columns.head(50))
