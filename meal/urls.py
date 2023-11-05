from django.urls import path
from .views import MealView, MealRetrieveDestroyView, MealUpdateView


urlpatterns = [
    path('meal/add/', MealView.as_view(), name='customer-meal-add'),
    path('meal/<pk>/', MealRetrieveDestroyView.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='customer-meal'),
    path('meal/update/<pk>/', MealUpdateView.as_view(), name='customer-meal'),
]
