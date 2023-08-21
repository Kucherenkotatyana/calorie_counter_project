from django.urls import path
from . import views


urlpatterns = [
    path('api/register/', views.CustomerRegistrationView.as_view(), name='customer-register'),
    path('api/customer/', views.CustomerDetailView.as_view(), name='customer-detail'),
]
