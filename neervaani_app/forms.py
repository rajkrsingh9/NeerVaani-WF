from django import forms
from .models import CropCalculator, Product

class CropCalculatorForm(forms.ModelForm):
    class Meta:
        model = CropCalculator
        fields = ['crop_name', 'land_size', 'land_unit', 'irrigation_method',
                  'rainfall_mm', 'irrigation_cycles', 'crop_yield', 'fertilizer_use',
                  'growing_season', 'avg_temperature']
        


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'green_water_footprint', 'blue_water_footprint', 'grey_water_footprint', 'total_water_footprint', 'description']
        




from django import forms

class WaterFootprintForm(forms.Form):
    SCALE_CHOICES = [('Small', 'Small-scale'), ('Medium', 'Medium-scale'), ('Large', 'Large-scale')]
    TEXTILE_CHOICES = [
        ('Garments', 'Garments'), 
        ('Home Textiles', 'Home Textiles'), 
        ('Industrial Textiles', 'Industrial Textiles'), 
        ('Others', 'Others')
    ]
    RAW_MATERIAL_CHOICES = [
        ('Cotton', 'Cotton'), ('Wool', 'Wool'), ('Polyester', 'Polyester'), 
        ('Silk', 'Silk'), ('Rayon', 'Rayon/Viscose'), ('Synthetic', 'Other Synthetic Fibers')
    ]
    WATER_SCARCE_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    AGRICULTURE_CHOICES = [('Rainfed', 'Rainfed'), ('Irrigated', 'Irrigated')]
    PROCESSES_CHOICES = [
        ('Dyeing', 'Dyeing'), ('Bleaching', 'Bleaching'), ('Washing', 'Washing'), 
        ('Printing', 'Printing'), ('Finishing', 'Finishing')
    ]
    ETP_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    RECYCLING_CHOICES = [
        ('Less than 25%', 'Less than 25%'), ('25–50%', '25–50%'), 
        ('51–75%', '51–75%'), ('More than 75%', 'More than 75%')
    ]
    DISPOSAL_CHOICES = [
        ('Reused', 'Reused in production'), 
        ('Released', 'Released into natural water bodies'), 
        ('Municipal', 'Sent to a municipal treatment facility')
    ]
    CHEMICAL_LOAD_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    DYE_CHOICES = [
        ('Natural', 'Natural dyes'), 
        ('Synthetic', 'Synthetic dyes'), 
        ('Biodegradable', 'Biodegradable chemicals'), 
        ('Non-Biodegradable', 'Non-biodegradable chemicals')
    ]
    STANDARD_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    TECHNOLOGY_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    MEASURE_CHOICES = [
        ('Meters', 'Installation of water meters'),
        ('Low-liquor', 'Low-liquor dyeing methods'),
        ('Reverse Osmosis', 'Reverse osmosis for recycling'),
        ('Awareness', 'Awareness and training programs')
    ]

    scale = forms.ChoiceField(choices=SCALE_CHOICES, label="Scale of Operations")
    textile_type = forms.ChoiceField(choices=TEXTILE_CHOICES, label="Type of Textile Products")
    production_output = forms.FloatField(label="Average Annual Production Output")
    production_unit = forms.ChoiceField(choices=[('kg', 'kg'), ('tons', 'tons')], label="Unit")
    raw_material = forms.ChoiceField(choices=RAW_MATERIAL_CHOICES, label="Raw Materials")
    water_scarce_region = forms.ChoiceField(choices=WATER_SCARCE_CHOICES, label="Water-scarce Regions?")
    agriculture_type = forms.ChoiceField(choices=AGRICULTURE_CHOICES, label="Agriculture Type")
    processes = forms.MultipleChoiceField(choices=PROCESSES_CHOICES, widget=forms.CheckboxSelectMultiple, label="Water-Intensive Processes")
    water_usage = forms.FloatField(label="Total Water Usage")
    etp = forms.ChoiceField(choices=ETP_CHOICES, label="Effluent Treatment Plant?")
    recycling_percent = forms.ChoiceField(choices=RECYCLING_CHOICES, label="Water Recycled")
    disposal = forms.ChoiceField(choices=DISPOSAL_CHOICES, label="Treated Water Disposal")
    chemical_load = forms.ChoiceField(choices=CHEMICAL_LOAD_CHOICES, label="Chemical Load Measured?")
    dye_type = forms.ChoiceField(choices=DYE_CHOICES, label="Dyes and Chemicals Used")
    water_standards = forms.ChoiceField(choices=STANDARD_CHOICES, label="Compliant with Standards?")
    water_tech = forms.ChoiceField(choices=TECHNOLOGY_CHOICES, label="Water-efficient Technologies?")
    measures = forms.MultipleChoiceField(choices=MEASURE_CHOICES, widget=forms.CheckboxSelectMultiple, label="Measures Taken")
