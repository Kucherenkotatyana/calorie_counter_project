from rest_framework import serializers
from .models import Meal

from services.nutrition import ProductNotFoundException
from services.product_finder import ProductFinder


class MealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = [
            'id',
            'date_add',
            'meal_type',
            'product_name',
            'portion_size',
            'portion_calories',
        ]
        read_only_fields = [
            'id',
            'portion_calories',
        ]

    def create(self, validated_data):
        user = self.context['user']  # Get the current authenticated user

        product_calories = self._get_product_calories(validated_data)

        meal = Meal(
            user=user,
            date_add=validated_data['date_add'],
            meal_type=validated_data['meal_type'],
            product_name=validated_data['product_name'],
            portion_size=validated_data['portion_size'],
            portion_calories=int(round(validated_data['portion_size'] / 100 * product_calories)),
        )
        meal.save()
        return meal

    def _get_product_calories(self, product_data):
        try:
            product_finder = ProductFinder()
            calories = product_finder.find(product_data)
            return calories
        except ProductNotFoundException as e:
            raise serializers.ValidationError({"error": str(e)})


class MealUpdateSerializer(MealSerializer):

    class Meta:
        read_only_fields = ['id', 'date_add', 'product_name', 'portion_calories']
