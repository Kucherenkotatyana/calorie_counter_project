from django.shortcuts import get_object_or_404
from django.db import models

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
from meal.models import Meal
from activity.models import CustomerActivity

from datetime import date, datetime


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


class DailyStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer_id = request.user.id

        target = self.get_target(customer_id)
        total_calories = self.get_total_calories(customer_id)
        total_activity = self.get_total_activity(customer_id)
        calories_including_activity = self.get_calories_including_activity(
            total_calories,
            total_activity
        )
        percentage = self.get_percentage(calories_including_activity, target)
        response = self.create_response(
            target,
            total_calories,
            total_activity,
            calories_including_activity,
            percentage,
        )

        return Response(response, status=status.HTTP_200_OK)

    def get_target(self, customer_id):
        try:
            current_profile = get_object_or_404(
                CustomerProfile,
                customer=customer_id
            )
            target = current_profile.target
            return target
        except (ValueError, Exception):
            return "target wasn't set"

    def get_total_calories(self, customer_id):
        given_date = self.get_date_from_request()

        customer_meals = Meal.objects.filter(
            user=customer_id,
            date_add__year=given_date.year,
            date_add__month=given_date.month,
            date_add__day=given_date.day,
        )

        # total_calories = customer_meals.aggregate(
        #     total_calories=models.Sum('portion_calories') or 0
        # )

        total_calories = 0

        for meal in customer_meals:
            total_calories += int(meal.portion_calories)
        return total_calories

    def get_total_activity(self, customer_id):
        given_date = self.get_date_from_request()
        activities = CustomerActivity.objects.filter(
            customer=customer_id,
            date_add__date=given_date
        )
        # total_activity = activities.aggregate(
        #     total_calories=models.Sum('spent_calories') or 0
        # )

        total_activity = 0
        for activity in activities:
            total_activity += int(activity.spent_calories)
        return total_activity

    def get_date_from_request(self):
        input_date_add = self.request.query_params.get('date_add', None)

        if input_date_add:
            given_date = datetime.strptime(input_date_add, '%Y-%m-%d')
        else:
            given_date = date.today()
        return given_date

    def get_calories_including_activity(
            self,
            total_calories,
            total_activity
    ):
        calories_including_activity = total_calories - total_activity
        return calories_including_activity

    def get_percentage(self, calories_including_activity, target):
        percentage = int(calories_including_activity*100/target)
        return percentage

    def create_response(
            self,
            target,
            total_calories,
            total_activity,
            calories_including_activity,
            percentage,
    ):
        response = dict(
            target=target,
            total_calories=total_calories,
            total_activity=total_activity,
            calories_including_activity=calories_including_activity,
            percentage=percentage,
        )

        return response
