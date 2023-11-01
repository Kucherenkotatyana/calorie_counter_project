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

        try:
            current_meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user != current_meal.user:
            return Response(
                {"error": "Action not allowed."},
                status=status.HTTP_403_FORBIDDEN
            )

        incoming_data = request.data

        access_status, need_to_recalculate_calories = self._patch_request_validation(incoming_data)

        if not access_status:
            return Response(
                {
                    "error": ("Something was wrong in your request. It only needs to contain "
                              "'meal_type' and/or 'portion_size' arguments."),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif access_status and not need_to_recalculate_calories:
            try:
                self._update_meal(current_meal, incoming_data)
                response_data = self._create_response(current_meal, incoming_data, new_portion_calories=None)
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": f"Something went wrong updating 'meal_type': {e}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif access_status and need_to_recalculate_calories:
            try:
                new_portion_calories = self._recalculate_calories(current_meal, incoming_data)
                incoming_data["portion_calories"] = new_portion_calories
                response_data = self._create_response(current_meal, incoming_data, new_portion_calories)
                self._update_meal(current_meal, incoming_data)
                return Response(response_data, status=status.HTTP_200_OK)
            except (ProductNotFoundException, Exception) as e:
                return Response(
                    {
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            self._update_meal(current_meal, incoming_data)
        except InvalidSerializedData as e:
            return Response(
                    {
                        "error": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def _patch_request_validation(self, incoming_data):
        permitted_fields = ["meal_type",  "portion_size"]

        access_status = True
        need_to_recalculate_calories = False

        if incoming_data:
            for elem in incoming_data:
                if elem in permitted_fields:
                    continue
                else:
                    access_status = False
        else:
            access_status = False

        if "portion_size" in incoming_data:
            need_to_recalculate_calories = True

        return access_status, need_to_recalculate_calories

    def _recalculate_calories(self, current_meal, incoming_data):
        current_product_name = current_meal.product_name
        product_data = dict(product_name=current_product_name)

        product_finder = ProductFinder()
        calories = product_finder.find(product_data)

        new_portion_calories = int(round(incoming_data["portion_size"] / 100 * calories))

        return new_portion_calories

    def _update_meal(self, current_meal, new_data):
        serializer = MealSerializer(current_meal, data=new_data, partial=True)  # new_data = dict

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _create_response(self, current_meal, incoming_data, new_portion_calories):

        date_add = current_meal.date_add
        meal_type = current_meal.meal_type
        product_name = current_meal.product_name
        portion_size = current_meal.portion_size
        portion_calories = current_meal.portion_calories

        if "meal_type" in incoming_data:
            meal_type = incoming_data["meal_type"]

        if "portion_size" in incoming_data:
            portion_size = incoming_data["portion_size"]

        if new_portion_calories:
            portion_calories = new_portion_calories

        response_data = {
            "date_add": date_add,
            "meal_type": meal_type,
            "product_name": product_name,
            "portion_size": portion_size,
            "portion_calories": portion_calories
        }

        return response_data
