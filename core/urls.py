
from django.contrib import admin
from django.urls import path, include

from core import views as core_views
urlpatterns = [
    path('home/', core_views.home, name='home'),
    path('', core_views.index, name='index'),
]
