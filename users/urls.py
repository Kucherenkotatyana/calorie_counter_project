from django.urls import path
from . import views


urlpatterns = [
    path('customer/register/', views.CustomerRegistrationView.as_view(), name='customer-register'),
    path('customer/show-details/', views.CustomerRetrieveUpdateView.as_view(), name='customer-detail'),
]
