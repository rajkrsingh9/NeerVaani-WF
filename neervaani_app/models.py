from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User

class User(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    type_of_user = models.CharField(max_length=50, choices=[('farmer', 'Farmer'), ('organization', 'Organization'), ('normal user', 'Normal User')])
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the creation timestamp

    def __str__(self):
        return self.username



class OTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()




class CropCalculator(models.Model):
    user = models.ForeignKey('neervaani_app.User', on_delete=models.CASCADE, null=True, blank=True)  # Link to User table
    crop_name = models.CharField(max_length=100)
    land_size = models.FloatField()  # Stored in acres after conversion
    land_unit = models.CharField(max_length=10, choices=[
        ('katha', 'Katha'),
        ('acres', 'Acres'),
        ('bigha', 'Bigha'),
    ])
    irrigation_method = models.CharField(max_length=50, choices=[
        ('flood', 'Flood'),
        ('drip', 'Drip'),
        ('sprinkler', 'Sprinkler'),
        ('surface', 'Surface'),
        ('center_pivot', 'Center Pivot'),
    ])
    rainfall_mm = models.FloatField()
    irrigation_cycles = models.IntegerField()
    crop_yield = models.FloatField()  # Yield in kg/acre
    fertilizer_use = models.FloatField()  # Fertilizer in kg/acre
    growing_season = models.CharField(max_length=10, choices=[
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
    ])
    avg_temperature = models.FloatField()  # Average temperature in Celsius
    water_footprint = models.FloatField()  # Stored as liters per kilogram
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.user}"









































class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, unique=True)
    green_water_footprint = models.FloatField()
    blue_water_footprint = models.FloatField()
    grey_water_footprint = models.FloatField()
    total_water_footprint = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.product_name
    
    
    
# class Languages(models.Model):
#     id = models.AutoField(primary_key=True)
#     currLang=models.CharField()
#     user = models.ForeignKey('neervaani_app.User', on_delete=models.CASCADE, null=True, blank=True)  # Link to User table
    

    


