from django.contrib import admin

from .models import Dish, CuisineCategory

# Register your models here.
admin.site.register(Dish)
admin.site.register(CuisineCategory)

