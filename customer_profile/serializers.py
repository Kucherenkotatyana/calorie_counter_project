from rest_framework import serializers
from rest_framework.serializers import ValidationError
from customer_profile.models import CustomerProfile


def validate(customer):
    try:
        CustomerProfile.objects.get(customer=customer)
    except CustomerProfile.DoesNotExist:
        return
    else:
        raise ValidationError(['Customer already has a target'])


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['id', 'target']

    def create(self, validated_data):
        customer = self.context['user']

        validate(customer)

        customer_profile_note = CustomerProfile(
            customer=customer,
            target=validated_data['target'],
        )
        customer_profile_note.save()
        return customer_profile_note


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta(CustomerProfileSerializer.Meta):
        read_only_fields = [
            'id',
            'customer',
        ]

    def update(self, instance, validated_data):

        if 'target' in validated_data:
            return super().update(instance, validated_data)
