import pytest

from unittest.mock import Mock, patch
from services.nutrition import NutritionAPIClient, ProductNotFoundException, NutritionAPIException


@patch("services.nutrition.requests.get")
def test_nutrition_api_client_get_single_product_ok(mock_get, single_product_sample):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = single_product_sample
    mock_get.return_value = mock_response

    product_name = 'fried potato'
    client = NutritionAPIClient()

    response = client.get_single_product_calories(product_name)

    assert response == 307.3


@patch("services.nutrition.requests.get")
def test_nutrition_api_client_get_single_product_not_found_exception(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    product_name = 'fried potato'
    client = NutritionAPIClient()

    with pytest.raises(ProductNotFoundException) as expected_response:
        client.get_single_product_calories(product_name)
    assert str(expected_response.value) == "No such product in the database or invalid product's name."


@patch("services.nutrition.requests.get")
def test_nutrition_api_client_get_single_product_api_exception(mock_get):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_get.return_value = mock_response

    product_name = 'fried potato'
    client = NutritionAPIClient()

    with pytest.raises(NutritionAPIException) as expected_response:
        client.get_single_product_calories(product_name)
    assert str(expected_response.value) == "There's a problem with connection to API."


@patch("services.nutrition.requests.get")
def test_nutrition_api_client_get_multiple_products_calories_ok(mock_get, multiple_products_sample):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = multiple_products_sample
    mock_get.return_value = mock_response

    product_names = ['fried potato', 'onion']
    client = NutritionAPIClient()

    response = client.get_multiple_products_calories(product_names)

    assert response == {"fried potato": 307.3, "onion": 44.7}


@patch("services.nutrition.requests.get")
def test_nutrition_api_client_get_multiple_products_not_found_exception(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    product_names = ['fried potato', 'onion']
    client = NutritionAPIClient()

    with pytest.raises(ProductNotFoundException) as expected_response:
        client.get_multiple_products_calories(product_names)
    assert str(expected_response.value) == "No such product in the database or invalid product's name."


@patch("services.nutrition.requests.get")
def test_nutrition_api_client_get_multiple_products_calories_including_unknown_ok(mock_get, multiple_products_sample):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = multiple_products_sample
    mock_get.return_value = mock_response

    product_names = ['fried potato', 'unknown', 'onion']
    client = NutritionAPIClient()

    response = client.get_multiple_products_calories(product_names)

    assert response == {"fried potato": 307.3, "onion": 44.7}


@patch("services.nutrition.requests.get")
def test_nutrition_api_client_get_multiple_products_calories_api_exception(mock_get):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_get.return_value = mock_response

    product_names = ['fried potato', 'onion']
    client = NutritionAPIClient()

    with pytest.raises(NutritionAPIException) as expected_response:
        client.get_multiple_products_calories(product_names)
    assert str(expected_response.value) == "There's a problem with connection to API."
