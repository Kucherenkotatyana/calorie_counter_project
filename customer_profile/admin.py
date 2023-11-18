from django.contrib import admin
from .models import CustomerProfile


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'target',
    )


admin.site.register(CustomerProfile, CustomerProfileAdmin)
