from rest_framework import serializers
from .models import Meal

from meal.utils import get_product_calories


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
        user = self.context['user']    # Get the current authenticated user
        given_product = validated_data["product_name"]

        product_calories = get_product_calories(given_product)

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


class MealUpdateSerializer(MealSerializer):

    class Meta(MealSerializer.Meta):
        read_only_fields = [
            'id',
            'date_add',
            'product_name',
            'portion_calories',
        ]

    def update(self, instance, validated_data):
        given_product = instance.product_name

        if 'portion_size' in validated_data:
            product_calories = get_product_calories(given_product)
            validated_data['portion_calories'] = int(
                round(validated_data['portion_size'] / 100 * product_calories),
            )
        return super().update(instance, validated_data)
