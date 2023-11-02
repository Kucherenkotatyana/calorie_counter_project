import pytest

from unittest.mock import patch
from rest_framework.exceptions import ErrorDetail
from rest_framework import serializers

from meal.views import ProductNotFoundException
from meal.models import Meal


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_get_product_calories_ok(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the view works properly with valid data.
    """
    mock_get_product_calories.return_value = 5

    product_data = dict(
        date_add="2023-10-11T13:35:10Z",
        meal_type="LU",
        product_name="watermelon",
        portion_size=100,
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    meal_created = Meal.objects.first()

    assert response.status_code == 201
    assert meal_created.user.id == customer_id
    assert meal_created.date_add.strftime('%Y-%m-%dT%H:%M:%SZ') == product_data["date_add"]
    assert meal_created.meal_type == product_data["meal_type"]
    assert meal_created.product_name == product_data["product_name"]
    assert meal_created.portion_size == product_data["portion_size"]
    assert meal_created.portion_calories == 5.0


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_get_product_calories_product_not_found_exception(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the view returns a proper error while passing nonexistent product name.
    """
    mock_get_product_calories.side_effect = serializers.ValidationError({"error": "test error"})

    product_data = dict(
        date_add="2023-10-11T13:35:10Z",
        meal_type="LU",
        product_name="abracadabra",
        portion_size=100,
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {'error': 'test error'}


@pytest.mark.django_db
def test_meal_view_get_product_calories_no_customer(
        authenticated_client,
):
    """
    Testing if the view returns a proper error while passing nonexistent customer id.
    """
    customer_id = 150

    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data={},
        format='json',
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_meal_view_get_product_calories_wrong_customer(
        authenticated_client,
        another_authenticated_client
):
    """
    Testing if the view returns a proper error while passing a foreign customer id.
    """
    customer_id = 2

    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data={},
        format='json',
    )

    assert response.status_code == 403
    assert response.data == {"error": "Action not allowed."}


@pytest.mark.django_db
def test_meal_view_get_product_calories_no_product_name(
        authenticated_client
):
    """
    Testing if the view returns a proper error if there's no product_name in request.
    """
    product_data = dict(
        date_add="2023-10-11T13:35:10Z",
        meal_type="LU",
        portion_size=100,
    )

    customer_id = 1

    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        "product_name": [
            "This field is required."
        ]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_get_product_calories_missed_portion_size(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the view returns a proper error if there's no portion_size in request.
    """
    mock_get_product_calories.return_value = 5

    product_data = dict(
        date_add="2023-10-11T13:35:10Z",
        meal_type="LU",
        product_name="watermelon",
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        "portion_size": [
            "This field is required."
        ]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_get_product_calories_missed_meal_type(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the view returns a proper error if there's no meal_type in request.
    """
    mock_get_product_calories.return_value = 5

    product_data = dict(
        date_add="2023-10-11T13:35:10Z",
        product_name="watermelon",
        portion_size=100,
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        "meal_type": [
            "This field is required."
        ]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_get_product_calories_missed_date_add(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the view returns a proper error if there's no date_add in request.
    """
    mock_get_product_calories.return_value = 5

    product_data = dict(
        meal_type="LU",
        product_name="watermelon",
        portion_size=100,
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        "date_add": [
            "This field is required."
        ]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_create_meal_invalid_date_add_for_serializer(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the serializer returns a proper error while passing invalid date_add value.
    """
    mock_get_product_calories.return_value = 5

    product_data = dict(
        date_add="test",
        meal_type="LU",
        product_name="watermelon",
        portion_size=100,
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        'date_add':
            [ErrorDetail(string='Datetime has wrong format. Use one of these formats instead: '
                                'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].', code='invalid')]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_create_meal_invalid_meal_type_for_serializer(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the serializer returns a proper error while passing invalid meal_type value.
    """
    mock_get_product_calories.return_value = 5

    product_data = dict(
        date_add="2023-10-11T13:35:10Z",
        meal_type="test",
        product_name="watermelon",
        portion_size=100,
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        'meal_type': [ErrorDetail(string='"test" is not a valid choice.', code='invalid_choice')]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_create_meal_invalid_portion_size_for_serializer_passed_string(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the serializer returns a proper error while passing string inside portion_size (int was expected).
    """
    mock_get_product_calories.return_value = 5

    product_data = dict(
        date_add="2023-10-11T13:35:10Z",
        meal_type="DI",
        product_name="watermelon",
        portion_size="test",
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        "portion_size": [
            "A valid integer is required."
        ]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_view_create_meal_invalid_portion_size_for_serializer_passed_float(
        mock_get_product_calories,
        authenticated_client,
):
    """
    Testing if the serializer returns a proper error while passing float inside portion_size (int was expected).
    """
    mock_get_product_calories.return_value = 5

    product_data = dict(
        date_add="2023-10-11T13:35:10Z",
        meal_type="DI",
        product_name="watermelon",
        portion_size=55.5,
    )

    customer_id = 1  # id of the authenticated_client
    response = authenticated_client.post(
        f"/api/meal/add/{customer_id}/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        'portion_size': [ErrorDetail(string='A valid integer is required.', code='invalid')]
    }

