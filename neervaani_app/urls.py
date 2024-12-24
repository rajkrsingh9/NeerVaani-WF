from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.view_profile, name='view_profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('insight/', views.insight, name='insight'),
    path('Chart/', views.Chart, name='Chart'),
    path('map2/', views.map2, name='map2'),
    path('piechart/', views.piechart, name='piechart'),
    path('crop_calculator/', views.crop_calculator, name='crop_calculator'),
    path('mycalculator/', views.mycalculator, name='mycalculator'),
    path('set-language/', views.set_language, name='set_language'),
    path('water-footprint/', views.water_footprint_view, name='water_footprint'),
    path('search/', views.search_product, name='search_product'),  # Search page
    path('add/', views.add_product, name='add_product'),           # Add product page
    
]

