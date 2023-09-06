from .models import CustomerActivity
from .serializers import CustomerActivitySerializer, CustomActivityResponseSerializer
from .permissions import IsOwner

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
    serializer_class = CustomActivityResponseSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def get(self, request):
        date_str = self.request.query_params.get('date', None)
        pk = self.request.query_params.get('pk', None)

        if not date_str or not pk:
            return Response(
                {"error": "Both 'date' and 'pk' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return Response(
                {"error": "Invalid date format. Please use 'YYYY-MM-DD'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        activities = CustomerActivity.objects.filter(customer=customer, date_add__date=date.date())

        if not activities:
            return Response(
                {"error": "No added activities for the chosen date"},
                status=status.HTTP_404_NOT_FOUND
            )

        total_calories = activities.aggregate(total_calories=models.Sum('spent_calories'))['total_calories'] or 0

        serialized_activities = CustomerActivitySerializer(activities, many=True)

        response_data = {
            "total_calories": total_calories,
            "records": serialized_activities.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
