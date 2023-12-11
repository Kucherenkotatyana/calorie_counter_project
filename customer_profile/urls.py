from django.urls import path
from .views import (
    CustomerProfileView,
    DailyStatisticsView,
)

urlpatterns = [
    path('customer-profile/<int:pk>/',
         CustomerProfileView.as_view(), name='customer-profile'),
    path('customer-daily-statistics/',
         DailyStatisticsView.as_view(), name='daily-statistics'),
]


