from product.models import Product
from product.serializers import ProductSerializer

from typing import List, Dict, Any

from .nutrition import NutritionAPIClient
from django.core.exceptions import ObjectDoesNotExist


class InvalidProductException(Exception):
    pass


class NoSuchProductInAPIDatabase(Exception):
    pass


class ProductFinder:

    def finder(self, data: Dict[str, Any]):
        given_product = data['product_name']

        database_result = self.search_in_database(given_product)

        if database_result:
            return database_result

        else:
            nutrition_api_result = self.search_in_nutrition_api(given_product)
            self.write_to_product_database(given_product, nutrition_api_result)
            return nutrition_api_result

    def search_in_database(self, given_product):

        try:
            product = Product.objects.get(name=given_product)
            calories = product.calories
            return calories

        except ObjectDoesNotExist:
            return

    def search_in_nutrition_api(self, given_product):

        nutrition_api_client = NutritionAPIClient()
        result = nutrition_api_client.get_single_product_calories(given_product)

        return result

    def write_to_product_database(self, given_product, calories):
        product = dict(name=given_product, calories=calories)

        serializer = ProductSerializer(data=product)

        if serializer.is_valid():
            serializer.save()
        else:
            raise InvalidProductException("Invalid given product.")

