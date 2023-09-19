from typing import List, Dict, Any

import requests
from Calorie_counter.settings import NUTRITION_API_KEY


class NutritionAPIException(Exception):
    pass


class ProductNotFoundException(Exception):
    pass


class NutritionAPIClient:

    API_URL = "https://api.api-ninjas.com/v1/nutrition"

    def get_single_product_calories(self, product_name: str) -> float:
        data = self._get_calories(product_name)
        product_calories = data[0]["calories"]
        return product_calories

    def get_multiple_products_calories(self, product_names: List[str]) -> Dict[str, float]:
        product_names = ', '.join(product_names)

        data = self._get_calories(product_names)

        products_calories = {}
        for item in data:
            products_calories[item["name"]] = item["calories"]
        return products_calories

    def _get_calories(self, query: str) -> List[Dict[str, Any]]:
        response = requests.get(
            f"{self.API_URL}?query={query}",
            headers={'X-Api-Key': NUTRITION_API_KEY},
        )
        if response.status_code == requests.codes.ok:
            data = response.json()
            if not data:
                raise ProductNotFoundException("No such product in the database or invalid product's name.")
            return data
        else:
            raise NutritionAPIException("There's a problem with connection to API.")
