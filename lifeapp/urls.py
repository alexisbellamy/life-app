from django.contrib import admin
from django.urls import path, include
from core import urls as core_urls
from pet import urls as pet_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include(core_urls)),
    path('', include(pet_urls)),
]
