"""
While testing NutritionAPIClient we are interested only in two params - 'name' and 'calories' for each product. In this
case it prevents our tests from other unimportant incoming params which could be changed by API's owners.
"""
import pytest
import json

from services.nutrition import NutritionAPIClient


@pytest.mark.django_db
def test_nutrition_api_client_get_single_product_ok():
    query = 'fried potato'

    client = NutritionAPIClient()

    response = client.get_single_product_calories(query)    # returns JSON String
    converted_data = json.loads(response)   # converts the JSON String document into the dictionary

    result = dict()

    for item in converted_data:
        result[item["name"]] = item["calories"]

    assert result == {"fried potato": 307.3}


@pytest.mark.django_db
def test_nutrition_api_client_get_single_product_empty_ok():
    query = ''

    client = NutritionAPIClient()

    response = client.get_single_product_calories(query)
    converted_data = json.loads(response)

    assert converted_data == []


@pytest.mark.django_db
def test_nutrition_api_client_get_single_product_unknown_product_ok():
    query = 'unknown product'

    client = NutritionAPIClient()

    response = client.get_single_product_calories(query)
    converted_data = json.loads(response)

    assert converted_data == []


@pytest.mark.django_db
def test_nutrition_api_client_get_multiple_products_calories_ok():
    query = 'fried potato, tomato'

    client = NutritionAPIClient()

    response = client.get_single_product_calories(query)
    converted_data = json.loads(response)

    result = dict()

    for item in converted_data:
        result[item["name"]] = item["calories"]

    assert result == {"fried potato": 307.3, "tomato": 18.2}


@pytest.mark.django_db
def test_nutrition_api_client_get_multiple_products_calories_including_unknown_ok():
    query = 'fried potato, unknown, tomato'

    client = NutritionAPIClient()

    response = client.get_single_product_calories(query)
    converted_data = json.loads(response)

    result = dict()

    for item in converted_data:
        result[item["name"]] = item["calories"]

    assert result == {"fried potato": 307.3, "tomato": 18.2}
