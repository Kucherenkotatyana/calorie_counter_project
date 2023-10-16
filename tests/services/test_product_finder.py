import pytest

from unittest.mock import Mock, patch
from rest_framework.exceptions import ErrorDetail

from product.models import Product
from services.product_finder import ProductFinder, InvalidProductException


@pytest.mark.django_db
def test_product_finder_find_in_product_db():
    """
    Testing if ProductFinder searches the product in the Product database.
    """
    Product.objects.create(name="test_product", calories=20.5)

    test_product = {"product_name": "test_product"}
    product_finder = ProductFinder()
    result = product_finder.find(test_product)

    assert result == 20.5


@pytest.mark.django_db
@patch("services.product_finder.NutritionAPIClient")
def test_product_finder_find_in_api_client_ok(
        mock_nutrition_api_client_class,
):
    """
    Testing if ProductFinder searches the product in the NutritionAPIClient
    and creates a new product in the Product database if the request was successful.
    """
    mock_calories = 33.3

    mock_nutrition_api_client_instance = Mock()
    mock_nutrition_api_client_instance.get_single_product_calories.return_value = mock_calories
    mock_nutrition_api_client_class.return_value = mock_nutrition_api_client_instance

    test_product = {"product_name": "test_product"}
    product_finder = ProductFinder()
    result = product_finder.find(test_product)

    created_product = Product.objects.first()

    assert result == mock_calories
    assert created_product.name == "test_product"
    assert created_product.calories == 33.3


@pytest.mark.django_db
@patch("services.product_finder.NutritionAPIClient")
def test_product_finder_find_in_api_client_not_found(
        mock_nutrition_api_client_class,
):
    """
    Testing if ProductFinder searches the product in the NutritionAPIClient
    and doesn't create a new product in the Product database when the request wasn't successful.
    """
    mock_nutrition_api_client_instance = Mock()
    mock_nutrition_api_client_instance.get_single_product_calories.return_value = Exception
    mock_nutrition_api_client_class.return_value = mock_nutrition_api_client_instance

    test_product = {"product_name": "test_product"}
    product_finder = ProductFinder()

    with pytest.raises(InvalidProductException) as expected_response:
        product_finder.find(test_product)

    created_product = Product.objects.first()

    assert str(expected_response.value) == str(InvalidProductException('Invalid given product.'))
    assert created_product is None
