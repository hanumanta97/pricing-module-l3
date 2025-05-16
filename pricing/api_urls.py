from django.urls import path
from . import views

urlpatterns = [
    path('simple-price/', views.simple_calculate_price, name='simple_calculate_price'),
]
