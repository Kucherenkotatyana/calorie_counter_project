from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.CustomerRegistrationView.as_view(), name='customer-register'),
    path('show-details/', views.CustomerRetrieveUpdateView.as_view(), name='customer-detail'),
]
