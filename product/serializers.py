from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'calories']

    def create(self, validated_data):
        new_product = Product(
            name=validated_data['name'],
            calories=validated_data['calories']
        )
        new_product.save()
        return new_product
