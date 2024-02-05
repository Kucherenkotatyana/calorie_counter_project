from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins

from .serializers import (
    MealSerializer,
    MealUpdateSerializer,
    # MealReadSerializer,
)
from .permissions import IsOwner
from users.models import Customer
from meal.models import Meal
from services.nutrition import ProductNotFoundException    # needed for tests

from datetime import date, datetime


class InvalidSerializedData(Exception):
    pass


class InvalidPassedData(Exception):
    def __str__(self):
        return ("Something was missed in your request. "
                "Check if it has: 'date_add', 'meal_type', "
                "'product_name' and 'portion_size' arguments.")


class MealView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer = get_object_or_404(
            Customer,
            pk=request.data.get("customer")
        )

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MealSerializer(
            data=request.data,
            context={"user": customer}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MealRetrieveDestroyView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Meal.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = MealSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class MealUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        current_meal = get_object_or_404(Meal, pk=pk)

        if request.user != current_meal.user:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MealUpdateSerializer(
            current_meal,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class MealListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            customer_meals = self.get_meals(pk)
        except (ValueError, Exception):
            return Response(
                {"error": "Wrong date format! YYYY-MM-DD is needed."},
                status=status.HTTP_403_FORBIDDEN,
            )

        response_data = self.create_response(customer_meals)

        return Response(response_data, status=status.HTTP_200_OK)

    def get_meals(self, customer_id):
        input_date_add = self.request.query_params.get('date_add', None)

        if input_date_add:
            given_date = datetime.strptime(input_date_add, '%Y-%m-%d')
        else:
            given_date = date.today()

        customer_meals = Meal.objects.filter(
            user=customer_id,
            date_add__year=given_date.year,
            date_add__month=given_date.month,
            date_add__day=given_date.day,
        )

        return customer_meals

    def create_response(self, customer_meals):

        breakfast_list = []
        lunch_list = []
        dinner_list = []

        response_data = {
            "breakfast": {
                "total": 0,
                "records": breakfast_list
            },
            "lunch": {
                "total": 0,
                "records": lunch_list
            },
            "dinner": {
                "total": 0,
                "records": dinner_list
            },
        }

        for meal in customer_meals:
            meal_object = {
                    "id": meal.id,
                    "date_add": meal.date_add,
                    "product_name": meal.product_name,
                    "portion_size": meal.portion_size,
                    "portion_calories": meal.portion_calories
            }
            if meal.meal_type == "BR":
                breakfast_list.append(meal_object)
                response_data["breakfast"]["total"] += int(meal.portion_calories)

            elif meal.meal_type == "LU":
                lunch_list.append(meal_object)
                response_data["lunch"]["total"] += int(meal.portion_calories)

            elif meal.meal_type == "DI":
                dinner_list.append(meal_object)
                response_data["dinner"]["total"] += int(meal.portion_calories)

        return response_data
