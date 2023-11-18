from rest_framework import serializers
from customer_profile.models import CustomerProfile


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['id', 'target']

    def create(self, validated_data):
        customer = self.context['request'].user

        customer_profile_note = CustomerProfile(
            customer=customer,
            target=validated_data['target'],
        )
        customer_profile_note.save()
        return customer_profile_note
