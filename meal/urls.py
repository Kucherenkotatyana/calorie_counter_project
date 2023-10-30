from django.urls import path
from .views import MealView


urlpatterns = [
    path('meal/add/<pk>/', MealView.as_view(), name='customer-meal-add'),
]
