
from django.contrib import admin
from django.urls import path, include
import pet.views as views

urlpatterns = [
    path('pets/<str:pet_name>/', views.pet),
    path('pet/needs', views.needs),
    path('pet/food', views.food)
]
