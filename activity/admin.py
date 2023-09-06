from django.contrib import admin
from .models import CustomerActivity


class CustomerActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_add', 'spent_calories')


admin.site.register(CustomerActivity, CustomerActivityAdmin)
