from rest_framework import serializers
from .models import Meal


class MealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = ['id', 'date_add', 'meal_type', 'product_name', 'portion_size', 'portion_calories']

    def create(self, validated_data):
        user = self.context['user']  # Get the current authenticated user

        meal_note = Meal(
            user=user,
            date_add=validated_data['date_add'],
            meal_type=validated_data['meal_type'],
            product_name=validated_data['product_name'],
            portion_size=validated_data['portion_size'],
            portion_calories=validated_data['portion_calories'],
        )
        meal_note.save()
        return meal_note
