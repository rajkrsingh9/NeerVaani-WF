import pandas as pd
import numpy as np
from neervaani_app.models import Product

# Step 1: Load the Excel file
excel_file = r'C:/Users/rajku/Downloads/Water Footprint Products.xlsx'
df = pd.read_excel(excel_file)

# Step 2: Normalize product names
df['product_name'] = df['product_name'].str.lower().str.strip()

# Step 3: Map similar names to a standard form
# name_mapping = {
#     'bananas': 'banana',
#     'banana, raw': 'banana',
#     # Add other mappings as needed
# }
# df['product_name'] = df['product_name'].replace(name_mapping)

# Step 4: Remove duplicates
df = df.drop_duplicates(subset='product_name', keep='first')

columns_to_fill = [
    'green_water_footprint', 
    'blue_water_footprint', 
    'grey_water_footprint', 
    'total_water_footprint'
]
df[columns_to_fill] = df[columns_to_fill].fillna(0)

# Step 5: Replace NaN with None
df = df.replace({np.nan: None})
# df = df.fillna(value=None)

# Step 6: Import data into the database
for _, row in df.iterrows():
    if not Product.objects.filter(product_name=row['product_name']).exists():
        Product.objects.create(
            product_name=row['product_name'],
            green_water_footprint=row['green_water_footprint'],
            blue_water_footprint=row['blue_water_footprint'],
            grey_water_footprint=row['grey_water_footprint'],
            total_water_footprint=row['total_water_footprint'],
            description=row['description']
        )

print("Data imported successfully!")
