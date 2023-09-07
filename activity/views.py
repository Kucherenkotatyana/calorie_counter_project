from .models import CustomerActivity
from .serializers import CustomerActivitySerializer
from .permissions import IsOwner

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import Customer
from django.db import models
from datetime import datetime


class CustomerActivityViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = CustomerActivity.objects.all()
    serializer_class = CustomerActivitySerializer
    permission_classes = [IsOwner, IsAuthenticated]


class CustomerActivitySummarizeData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        date_str = self.request.query_params.get('date', None)

        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Please use 'YYYY-MM-DD'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            date = datetime.now()

        activities = CustomerActivity.objects.filter(customer=customer, date_add__date=date.date())
        total_calories = activities.aggregate(total_calories=models.Sum('spent_calories'))['total_calories'] or 0
        serialized_activities = CustomerActivitySerializer(activities, many=True)

        response_data = {
            "total_calories": total_calories,
            "records": serialized_activities.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
