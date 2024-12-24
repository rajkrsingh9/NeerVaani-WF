import pandas as pd
from neervaani_app.models import WaterScarcity
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neervaani.settings')
django.setup()

# Map categories to numerical values
category_to_value = {
    "No Stress [>1700 m³]": 1700,
    "Stress [1000−1700 m³]": 1500,
    "Scarcity [500−1000 m³]": 750,
    "Absolute scarcity [<500 m³]": 500,
}

# Load the Excel file
file_path = r'C:/Users/rajku\Downloads/Per_Capita_Water_Availability_2025_&_2050_1732427498344 (1).xlsx'
data = pd.read_excel(file_path)

# Import data into WaterScarcity model
for _, row in data.iterrows():
    value_2025 = category_to_value.get(row['Value for 2025'], 0)
    value_2050 = category_to_value.get(row['Value for 2050'], 0)
    WaterScarcity.objects.create(
        state=row['State'],
        district=row['District'],
        value_2025=row['Value for 2025'],
        value_2050=row['Value for 2050'],
        value_2025_value=value_2025,
        value_2050_value=value_2050,
    )

print("Data imported successfully!")
