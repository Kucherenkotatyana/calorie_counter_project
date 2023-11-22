from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CustomerProfile
from .serializers import (
    CustomerProfileSerializer,
    CustomerProfileUpdateSerializer,
)
from users.models import Customer


class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            current_profile = get_object_or_404(CustomerProfile, customer=pk)
            serialised_profile = CustomerProfileSerializer(current_profile)
            return Response(serialised_profile.data, status=status.HTTP_200_OK)
        except (ValueError, Exception) as e:
            return Response(
                {f"{e} Check if you passed a valid customer id."},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CustomerProfileSerializer(
            data=request.data,
            context={"user": customer}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            current_profile = get_object_or_404(CustomerProfile, customer=pk)
        except (ValueError, Exception) as e:
            return Response(
                {f"{e} You can change only existing profile!"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerProfileUpdateSerializer(
            current_profile,
            data=request.data,
            partial=True,
        )

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, Exception) as e:
            return Response(
                {f"{e}. You need to pass a valid integer to update your target!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            current_profile = get_object_or_404(CustomerProfile, customer=pk)
        except (ValueError, Exception) as e:
            return Response(
                {f"{e} No such profile data was found!"},
                status=status.HTTP_404_NOT_FOUND
            )

        current_profile.delete()
        return Response({"Deleted."}, status=status.HTTP_204_NO_CONTENT)
