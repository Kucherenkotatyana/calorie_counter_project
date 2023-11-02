from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins

from services.nutrition import ProductNotFoundException
from .serializers import MealSerializer, MealUpdateSerializer
from .permissions import IsOwner
from services.product_finder import ProductFinder
from users.models import Customer
from meal.models import Meal


class InvalidSerializedData(Exception):
    pass


class InvalidPassedData(Exception):
    def __str__(self):
        return ("Something was missed in your request. Check if it has: 'date_add', "
                "'meal_type', 'product_name' and 'portion_size' arguments.")


class MealView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer = get_object_or_404(Customer, pk=request.data.get("customer"))

        if request.user != customer:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MealSerializer(data=request.data, context={"user": customer})
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
