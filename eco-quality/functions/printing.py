def print_collection(collection):
    """Function to print the collection"""
    for i, c in enumerate(collection):
        print(f"{i}. {c['name']} - {c['url']}")
        print(f"Category: {c['category']}")
        print(f"Subcategory: {c['subcategory']}")
        print(f"Subsubcategory: {c['sub_subcategory']} \n")

def print_product(product):
    """Function to print the product"""
    for key, value in product.items():
        print(f"{key}: {value}")
