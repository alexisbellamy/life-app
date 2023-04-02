from django.contrib import admin

from .models import Pet, PetHeight, PetNeeds
# Register your models here.
admin.site.register(Pet)
admin.site.register(PetHeight)
admin.site.register(PetNeeds)