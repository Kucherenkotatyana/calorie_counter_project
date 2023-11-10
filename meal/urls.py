from django.urls import path
from .views import (
    MealView,
    MealRetrieveDestroyView,
    MealUpdateView,
    MealListView,
    # DenysMealListView,
)


urlpatterns = [
    # path('meal/denyslistview/<pk>/', DenysMealListView.as_view(), name='customer-denyslistview'),
    path('meal/listview/<pk>/', MealListView.as_view(), name='customer-listview'),
    path('meal/add/', MealView.as_view(), name='customer-meal-add'),
    path('meal/<pk>/', MealRetrieveDestroyView.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='customer-meal'),
    path('meal/update/<pk>/', MealUpdateView.as_view(), name='customer-meal'),
]
