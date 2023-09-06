from rest_framework import serializers
from .models import CustomerActivity


class CustomerActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerActivity
        fields = ['id', 'date_add', 'spent_calories']

    def create(self, validated_data):
        customer = self.context['request'].user  # Get the current authenticated user

        activity_note = CustomerActivity(
            customer=customer,
            date_add=validated_data['date_add'],
            spent_calories=validated_data['spent_calories']
        )
        activity_note.save()
        return activity_note


class CustomActivityResponseSerializer(serializers.Serializer):
    total_calories = serializers.IntegerField()
    records = CustomerActivitySerializer(many=True)
