from functions.processing_functions.handle_title import (get_model_from_title, get_package_from_title, remove_pending_spec)
from functions.processing_functions.handle_description import (clean_description, extract_sizes, extract_material, extract_volume, set_product_value)
from functions.processing_functions.handle_toilet_paper import (set_number_of_plies, set_number_of_rolls)
from functions.processing_functions.new_template import set_data_new_template

import params as params

print("Processing the data...")

############ Handling the title ############
# 1. Get the model from the title
try:
  get_model_from_title(params.INPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
  print("\nException at getting model from title\n")
  print(e)

# 2. Get the package details from the title
try:
  get_package_from_title(params.OUTPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
  print("\nException at getting package from title\n")
  print(e)

# 3. Remove the pending "()" spec from title
try:
  remove_pending_spec(params.OUTPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
    print("\nException at removing pending spec from title\n")
    print(e)
############################################

######## Handling the description ##########
# 1. Clean the description
try:
  clean_description(params.OUTPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
  print("\nException at cleaning description\n")
  print(e)

# 2. Extract the size from the description|title
try:
  extract_sizes(params.OUTPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
  print("Exception at extracting sizes")
  print(e)

# 3. Extract the material from the description
try:
  extract_material(params.OUTPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
  print("Exception at extracting material")
  print(e)

# 4. Extract the volume from the description|title
try:
  extract_volume(params.OUTPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
  print("Exception at extracting volume")
  print(e)

# 5. Extract the product value
try:
  set_product_value(params.OUTPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
  print("Exception at extracting product value")
  print(e)
############################################

######## Handling toilet paper #############
# 1. Set the number of plies
try:
  set_number_of_plies(params.OUTPUT_PATH_PROCESSING, params.OUTPUT_PATH_PROCESSING)
except Exception as e:
  print("Exception at setting number of plies")
  print(e)

# 2. Set the number of rolls
try:
  set_number_of_rolls(params.OUTPUT_PATH_PROCESSING, params.FINAL_OUTPUT_PATH_PROCESSING_CSV, params.FINAL_OUTPUT_PATH_PROCESSING_XLSX)
except Exception as e:
  print("\nException at setting number of rolls")
  print(f"{e}\n")
############################################

######## New format template ###############
try:
    set_data_new_template(params.FINAL_OUTPUT_PATH_PROCESSING_CSV, params.FINAL_OUTPUT_PATH_PROCESSING_CSV)
except Exception as e:
    print("\nException at setting new template\n")
    print(e)
############################################

print("Data processing complete!")
