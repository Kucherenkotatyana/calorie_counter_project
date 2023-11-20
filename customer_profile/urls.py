from django.urls import path
from .views import (
    CustomerProfileView,
)

urlpatterns = [
    path('customer-profile/<int:pk>/',
         CustomerProfileView.as_view(), name='customer-profile'),
]
