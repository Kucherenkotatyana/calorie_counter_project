import requests
from Calorie_counter.settings import NUTRITION_API_KEY

import json


class NutritionAPIClient:
    """
    Takes a string with products and returns a JSON String if the operation was successful.
    Returns an empty list if there's no such product in the NutritionAPI's database.
    """

    def get_single_product_calories(self, query):
        api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
        response = requests.get(api_url, headers={'X-Api-Key': NUTRITION_API_KEY})

        if response.status_code == requests.codes.ok:
            return response.text    # # returns JSON String
        else:
            return f'Error: {response.status_code}, {response.text}'

    def get_multiple_products_calories(self, query):
        api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
        response = requests.get(api_url, headers={'X-Api-Key': NUTRITION_API_KEY})

        if response.status_code == requests.codes.ok:
            return response.text    # returns JSON String
        else:
            return f'Error: {response.status_code}, {response.text}'
