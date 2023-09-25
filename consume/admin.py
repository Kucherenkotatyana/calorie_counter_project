from django.contrib import admin
from .models import Meal


class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_add', 'meal_type', 'product_name', 'portion_size', 'total_calories')


admin.site.register(Meal, MealAdmin)
