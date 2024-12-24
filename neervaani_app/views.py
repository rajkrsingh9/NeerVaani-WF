from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, OTP, Product, CropCalculator 
from django.http import JsonResponse
from django.shortcuts import redirect
from .utils import generate_otp
from datetime import datetime
from .forms import CropCalculatorForm
from googletrans import Translator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required 
from django.utils import timezone  # Import timezone


def set_language(request):
    language = request.GET.get('language', 'en')
    response = JsonResponse({'message': 'Language set successfully'})
    response.set_cookie('selected_language', language, max_age=30 * 24 * 60 * 60)  # Cookie valid for 30 days
    return response
    
    
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')  # Redirect to your login page
        return view_func(request, *args, **kwargs)
    return wrapper 


# Home page view
def home(request):
    return render(request, 'home.html')

def insight(request):
    return render(request, 'insight.html')

def Chart(request):
    return render(request, 'Chart.html')



def map2(request):
    return render(request, 'map2.html')

def piechart(request):
    return render(request, 'piechart.html')



def dashboard(request):
    return render(request, 'dashboard.html')



def signup(request):
    if request.method == 'POST':
        userid = request.POST['userid']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone']
        password = make_password(request.POST['password'])
        user_type = request.POST['type_of_user']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')
        
        user = User(userid=userid, username=username, email=email, phone_number=phone_number,
                    password=password, type_of_user=user_type, city=city, state=state, pincode=pincode)
        user.save()
        messages.success(request, "Signup successful! Please login.")
        return redirect('login')
    return render(request, 'signup.html')



def login(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']  # userid or email
        password = request.POST['password']
        try:
            user = User.objects.get(email=identifier) if '@' in identifier else User.objects.get(userid=identifier)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid password!")
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")
    return render(request, 'login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            generate_otp(email)
            messages.success(request, "OTP sent to your email!")
            return redirect('reset_password')  # Redirect to reset password page
        except User.DoesNotExist:
            messages.error(request, "No account found with this email!")
    return render(request, 'forgot_password.html')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, "Logged out successfully!")
    return redirect('login')

def view_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    return render(request, 'profile.html', {'user': user})



def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp_code = request.POST['otp']
        new_password = request.POST['password']
        try:
            otp_entry = OTP.objects.get(email=email, otp_code=otp_code)
            if timezone.now() > otp_entry.expires_at:  # Use timezone.now() here
                messages.error(request, "OTP has expired!")
                return redirect('forgot_password')
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            otp_entry.delete()  # Clean up OTP entry after successful reset
            messages.success(request, "Password reset successfully!")
            return redirect('login')
        except (OTP.DoesNotExist, User.DoesNotExist):
            messages.error(request, "Invalid OTP or email!")
    return render(request, 'reset_password.html')





from django.shortcuts import render
from .forms import CropCalculatorForm
from .models import CropCalculator

def convert_land_size_to_acres(size, unit):
    """
    Convert land size from selected unit to acres.
    """
    conversion_factors = {
        'katha': 0.033,
        'acres': 1,
        'bigha': 1.613,
    }
    return size * conversion_factors.get(unit, 1)  # Default to 1 for acres


def calculate_water_footprint(land_size_acres, irrigation_method, rainfall_mm, irrigation_cycles, crop_yield,
                               fertilizer_use, growing_season, avg_temperature):
    """
    Calculate water footprint and return as liters per kg.
    """
    irrigation_efficiency = {
        'flood': 0.6,
        'drip': 0.9,
        'sprinkler': 0.8,
        'surface': 0.7,
        'center_pivot': 0.85,
    }
    season_factor = {
        'summer': 1.2,
        'winter': 1.0,
        'monsoon': 0.8,
    }
    temperature_factor = 1 + (avg_temperature - 25) * 0.02  # Adjust for temperature deviation from 25°C
    base_water_use = 1000  # Base water needed per acre in cubic meters
    efficiency = irrigation_efficiency.get(irrigation_method, 0.7)
    effective_rainfall = rainfall_mm * 0.001  # Convert mm to meters

    water_usage_cubic_meters = (
        ((base_water_use / efficiency) - effective_rainfall)
        * irrigation_cycles
        * land_size_acres
        * season_factor.get(growing_season, 1)
        * temperature_factor
    )
    water_usage_liters = water_usage_cubic_meters * 1000  # Convert to liters
    return water_usage_liters / max(crop_yield, 1)  # Avoid division by zero

def fetch_weather_data(lat, lon):
    api_key = "6a9d67f2066cc650d170a368dc2c32e8"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    temperature = response['main']['temp']
    rainfall = response.get('rain', {}).get('1h', 0)
    return temperature, rainfall

def crop_calculator(request):
    if request.method == 'POST':
        form = CropCalculatorForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            # Assign user if logged in, or default to "0000"
            crop.user = request.User if request.user.is_authenticated else None
            
            crop.land_size = convert_land_size_to_acres(form.cleaned_data['land_size'], form.cleaned_data['land_unit'])
            crop.water_footprint = calculate_water_footprint(
                crop.land_size,
                crop.irrigation_method,
                crop.rainfall_mm,
                crop.irrigation_cycles,
                crop.crop_yield,
                crop.fertilizer_use,
                crop.growing_season,
                crop.avg_temperature,
            )
            crop.save()
            return render(request, 'result.html', {'crop': crop})
    else:
        form = CropCalculatorForm()  # Display the form for a GET request
    return render(request, 'crop_calculator.html', {'form': form})




def mycalculator(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        drinking_water = int(request.POST.get('drinking_water', 0))
        shower_minutes = int(request.POST.get('shower_minutes', 0))
        bucket_size = int(request.POST.get('bucket_size', 0))
        buckets = int(request.POST.get('buckets', 0))
        clothes_washing = int(request.POST.get('clothes_washing', 0))
        washing_machine_water = int(request.POST.get('washing_machine_water', 0))
        toilet_flushes = int(request.POST.get('toilet_flushes', 0))
        cooking_water = int(request.POST.get('cooking_water', 0))
        vehicle_wash = int(request.POST.get('vehicle_wash', 0))
        rice = int(request.POST.get('rice', 0))
        wheat = int(request.POST.get('wheat', 0))
        fruits_vegetables = int(request.POST.get('fruits_vegetables', 0))
        milk = int(request.POST.get('milk', 0))
        eggs = int(request.POST.get('eggs', 0))
        clothes_yearly = int(request.POST.get('clothes_yearly', 0))

        # Direct water usage calculations
        direct_usage = (
            drinking_water * 30 +
            shower_minutes * 8 * 30 +
            bucket_size * buckets * 30 +
            clothes_washing * washing_machine_water +
            toilet_flushes * 8 * 30 +
            cooking_water * 30 +
            vehicle_wash * 4
        )

        # Indirect water usage calculations
        indirect_usage = (
            rice * 2.5 * 1000 +
            wheat * 1.82 * 1000 +
            fruits_vegetables * 1000 +
            milk * 1000 +
            eggs * 200 +
            clothes_yearly * 2500
        )

        total_water_footprint = direct_usage + indirect_usage

        return JsonResponse({
            'name': name,
            'direct_usage': direct_usage,
            'indirect_usage': indirect_usage,
            'total_water_footprint': total_water_footprint,
        })

    return render(request, 'mycalculator.html')




def search_product(request):
    query = request.GET.get('name', '')
    products = None
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    return render(request, 'search_product.html', {'products': products, 'query': query})



from .forms import ProductForm

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product')  # Redirect after successful form submission
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})









from django.shortcuts import render
from .forms import WaterFootprintForm

def water_footprint_view(request):
    if request.method == 'POST':
        form = WaterFootprintForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # Simulate calculations
            total_water = data['water_usage'] * 1.2  # Example multiplier
            green_water = total_water * 0.5
            blue_water = total_water * 0.3
            grey_water = total_water * 0.2

            context = {
                'total_water': total_water,
                'green_water': green_water,
                'blue_water': blue_water,
                'grey_water': grey_water,
            }
            return render(request, 'popup_result.html', context)
    else:
        form = WaterFootprintForm()

    return render(request, 'form.html', {'form': form})
