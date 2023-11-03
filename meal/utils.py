from rest_framework import serializers

from services.nutrition import ProductNotFoundException
from services.product_finder import ProductFinder


def get_product_calories(given_product):
    try:
        product_finder = ProductFinder()
        calories = product_finder.find(given_product)
        return calories
    except ProductNotFoundException as e:
        raise serializers.ValidationError({"error": str(e)})
