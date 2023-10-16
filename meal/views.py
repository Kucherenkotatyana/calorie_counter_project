from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from services.nutrition import ProductNotFoundException
from .serializers import MealSerializer
from services.product_finder import ProductFinder
from users.models import Customer


class InvalidSerializedData(Exception):
    pass


class InvalidPassedData(Exception):
    def __str__(self):
        return ("Something was missed in your request. Check if it has: 'date_add', "
                "'meal_type', 'product_name' and 'portion_size' arguments.")


class MealView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        product_data = request.data

        if 'product_name' not in product_data:
            return Response(
                {
                    "error": ("Something was missed in your request. Check if it has: "
                              "'date_add', 'meal_type', 'product_name' and 'portion_size' arguments."),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product_calories = self._get_product_calories(product_data)
        except ProductNotFoundException as e:
            return Response(
                {
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response_data = self._calculate_and_create_response(product_data, product_calories)
        except (KeyError, Exception) as e:
            return Response(
                {"error": f"{e}. Something was missed in your request. Check if it has: 'date_add', "
                          f"'meal_type', 'product_name' and 'portion_size' arguments."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self._create_meal(response_data, request)

        return Response(response_data, status=status.HTTP_200_OK)

    def _get_product_calories(self, product_data):

        product_finder = ProductFinder()
        calories = product_finder.find(product_data)

        return calories

    def _calculate_and_create_response(self, product_data, product_calories):

        date_add = product_data['date_add']
        meal_type = product_data['meal_type']
        product_name = product_data['product_name']
        portion_size = product_data['portion_size']
        portion_calories = int(round(portion_size / 100 * product_calories))

        response_data = {
            "date_add": date_add,
            "meal_type": meal_type,
            "product_name": product_name,
            "portion_size": portion_size,
            "portion_calories": portion_calories
        }

        return response_data

    def _create_meal(self, response_data, request):
        customer = request.user
        serializer = MealSerializer(data=response_data, context={"user": customer})

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
