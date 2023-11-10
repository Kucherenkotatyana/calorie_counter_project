import pytest

from unittest.mock import patch
from rest_framework.exceptions import ErrorDetail
from rest_framework import serializers

from meal.views import ProductNotFoundException
from meal.serializers import MealSerializer, MealUpdateSerializer
from meal.models import Meal
from users.models import Customer

from datetime import datetime, timezone



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
        customer=1,
        date_add="2023-10-11T13:35:10Z",
        meal_type="LU",
        product_name="watermelon",
        portion_size=100,
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
        data=product_data,
        format='json',
    )

    meal_created = Meal.objects.first()

    assert response.status_code == 201
    assert meal_created.user.id == 1
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
        customer=1,
        date_add="2023-10-11T13:35:10Z",
        meal_type="LU",
        product_name="abracadabra",
        portion_size=100,
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
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

    response = authenticated_client.post(
        f"/api/meal/add/",
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

    response = authenticated_client.post(
        f"/api/meal/add/",
        data={
            "customer": 2,
        },
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
        customer=1,
        date_add="2023-10-11T13:35:10Z",
        meal_type="LU",
        portion_size=100,
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
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
        customer=1,
        date_add="2023-10-11T13:35:10Z",
        meal_type="LU",
        product_name="watermelon",
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
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
        customer=1,
        date_add="2023-10-11T13:35:10Z",
        product_name="watermelon",
        portion_size=100,
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
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
        customer=1,
        meal_type="LU",
        product_name="watermelon",
        portion_size=100,
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
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
        customer=1,
        date_add="test",
        meal_type="LU",
        product_name="watermelon",
        portion_size=100,
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
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
        customer=1,
        date_add="2023-10-11T13:35:10Z",
        meal_type="test",
        product_name="watermelon",
        portion_size=100,
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
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
        customer=1,
        date_add="2023-10-11T13:35:10Z",
        meal_type="DI",
        product_name="watermelon",
        portion_size="test",
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
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
        customer=1,
        date_add="2023-10-11T13:35:10Z",
        meal_type="DI",
        product_name="watermelon",
        portion_size=55.5,
    )

    response = authenticated_client.post(
        f"/api/meal/add/",
        data=product_data,
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        'portion_size': [ErrorDetail(string='A valid integer is required.', code='invalid')]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_retrieve_destroy_view_get_product_details_ok(
        mock_get_product_calories,
        authenticated_client,
        meal_data,
):
    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    response = authenticated_client.get(
        f"/api/meal/1/"
    )

    assert response.status_code == 200
    assert response.data == {
        'id': 1,
        'date_add': '2023-10-11T13:35:10Z',
        'meal_type': 'DI',
        'product_name': 'watermelon',
        'portion_size': 55,
        'portion_calories': 30.0
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_retrieve_destroy_view_get_product_details_forbidden(
        mock_get_product_calories,
        authenticated_client,
        another_authenticated_client,
        meal_data,
):

    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    response = another_authenticated_client.get(
        f"/api/meal/1/"
    )

    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied')
    }


@pytest.mark.django_db
def test_meal_retrieve_destroy_view_get_product_details_not_found(
        authenticated_client,
):
    response = authenticated_client.get(
        f"/api/meal/1/"
    )

    assert response.status_code == 404
    assert response.data == {
        "detail": "Not found."
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_retrieve_destroy_view_delete_product_details_ok(
        mock_get_product_calories,
        authenticated_client,
        meal_data,
):
    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    response = authenticated_client.delete(
        f"/api/meal/1/"
    )

    assert response.status_code == 204


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_retrieve_destroy_view_delete_product_details_forbidden(
        mock_get_product_calories,
        authenticated_client,
        another_authenticated_client,
        meal_data,
):
    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    response = another_authenticated_client.delete(
        f"/api/meal/1/"
    )

    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied')
    }


@pytest.mark.django_db
def test_meal_retrieve_destroy_view_delete_product_details_not_found(
        authenticated_client,
):
    response = authenticated_client.delete(
        f"/api/meal/1/"
    )

    assert response.status_code == 404
    assert response.data == {
        "detail": "Not found."
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_update_view_patch_product_details_ok(
        mock_get_product_calories,
        authenticated_client,
        meal_data,
):
    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    patched_data = dict(
        meal_type="DI",
        portion_size=333
    )

    response = authenticated_client.patch(
        f"/api/meal/update/1/",
        data=patched_data,
        format='json'
    )

    assert response.status_code == 200
    assert response.data == {
        'date_add': '2023-10-11T13:35:10Z',
        'id': 1,
        'meal_type': 'DI',
        'portion_calories': 10.0,
        'portion_size': 333,
        'product_name': 'watermelon'
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_update_view_patch_product_details_odd_fields_ok(
        mock_get_product_calories,
        authenticated_client,
        meal_data,
):
    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    patched_data = dict(
        meal_type="LU",
        portion_size=150,
        product_name="abracadabra",
        date_add="test_date",
    )

    response = authenticated_client.patch(
        f"/api/meal/update/1/",
        data=patched_data,
        format='json'
    )

    assert response.status_code == 200
    assert response.data == {
        'date_add': '2023-10-11T13:35:10Z',
        'id': 1,
        'meal_type': 'LU',
        'portion_calories': 4.0,
        'portion_size': 150,
        'product_name': 'watermelon'
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_update_view_patch_product_details_forbidden(
        mock_get_product_calories,
        authenticated_client,
        another_authenticated_client,
        meal_data,
):
    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    patched_data = dict(
        meal_type="LU",
        portion_size=150
    )

    response = another_authenticated_client.patch(
        f"/api/meal/update/1/",
        data=patched_data,
        format='json'
    )

    assert response.status_code == 403
    assert response.data == {'error': 'Action not allowed.'}


@pytest.mark.django_db
def test_meal_update_view_patch_product_details_not_found(
        authenticated_client,
):

    patched_data = dict()

    response = authenticated_client.patch(
        f"/api/meal/update/1/",
        data=patched_data,
        format='json'
    )

    assert response.status_code == 404
    assert response.data == {'detail': ErrorDetail(string='Not found.', code='not_found')}


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_update_view_patch_product_details_wrong_meal_type(
        mock_get_product_calories,
        authenticated_client,
        meal_data,
):
    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    patched_data = dict(
        meal_type="test",
        portion_size=150,
    )

    response = authenticated_client.patch(
        f"/api/meal/update/1/",
        data=patched_data,
        format='json'
    )

    assert response.status_code == 400
    assert response.data == {
        'meal_type': [ErrorDetail(string='"test" is not a valid choice.', code='invalid_choice')]
    }


@patch("meal.serializers.get_product_calories")
@pytest.mark.django_db
def test_meal_update_view_patch_product_details_wrong_portion_size_format(
        mock_get_product_calories,
        authenticated_client,
        meal_data,
):
    mock_get_product_calories.return_value = 3

    Meal.objects.create(**meal_data)

    patched_data = dict(
        portion_size="test",
    )

    response = authenticated_client.patch(
        f"/api/meal/update/1/",
        data=patched_data,
        format='json'
    )

    assert response.status_code == 400
    assert response.data == {
        'portion_size': [ErrorDetail(string='A valid integer is required.', code='invalid')]
    }


@pytest.mark.django_db
def test_meal_list_view_get_meals_has_meals_ok(
        authenticated_client,
        meal_data,
        meal_data_2,
        meal_data_3,
):
    Meal.objects.create(**meal_data)
    Meal.objects.create(**meal_data_2)
    Meal.objects.create(**meal_data_3)

    response = authenticated_client.get(
        f"/api/meal/listview/1/",
        {"date_add": '2023-10-11'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data == {
        'breakfast': {
            'total': 22,
            'records': [
                {
                    'id': 2,
                    'date_add': datetime(
                        2023,
                        10,
                        11,
                        13,
                        35,
                        10,
                        tzinfo=timezone.utc),
                    'product_name': 'coffee',
                    'portion_size': 250,
                    'portion_calories': 15.0},
                {
                    'id': 3,
                    'date_add': datetime(
                        2023,
                        10,
                        11,
                        10,
                        15,
                        6,
                        tzinfo=timezone.utc),
                    'product_name': 'tomato',
                    'portion_size': 100,
                    'portion_calories': 7.0
                }
            ]
        },
        'lunch': {
            'total': 0,
            'records': []
        },
        'dinner': {
            'total': 30,
            'records': [
                {
                    'id': 1,
                    'date_add': datetime(
                        2023,
                        10,
                        11,
                        13,
                        35,
                        10,
                        tzinfo=timezone.utc),
                    'product_name': 'watermelon',
                    'portion_size': 55,
                    'portion_calories': 30.0
                }
            ]
        }
    }


@pytest.mark.django_db
def test_meal_list_view_get_meals_no_meals_ok(
        authenticated_client,
):

    response = authenticated_client.get(
        f"/api/meal/listview/1/",
        {"date_add": '2023-10-11'},
        format='json',
    )

    assert response.status_code == 200
    assert response.data == {
        'breakfast': {
            'records': [],
            'total': 0
        },
        'dinner': {
            'records': [],
            'total': 0
        },
        'lunch': {
            'records': [],
            'total': 0}
    }


@pytest.mark.django_db
def test_meal_list_view_get_meals_no_date_add_passed_ok(
        authenticated_client,
):

    response = authenticated_client.get(
        f"/api/meal/listview/1/",
    )

    assert response.status_code == 200
    assert response.data == {
        'breakfast': {
            'records': [],
            'total': 0
        },
        'dinner': {
            'records': [],
            'total': 0
        },
        'lunch': {
            'records': [],
            'total': 0}
    }


@pytest.mark.django_db
def test_meal_list_view_get_meals_wrong_user(
        authenticated_client,
        another_authenticated_client
):

    response = authenticated_client.get(
        f"/api/meal/listview/2/",
    )

    assert response.status_code == 403
    assert response.data == {'error': 'Action not allowed.'}


@pytest.mark.django_db
def test_meal_list_view_get_meals_wrong_date_format(
        authenticated_client,
):

    response = authenticated_client.get(
        f"/api/meal/listview/1/",
        {"date_add": '2023-21-11'},
        format='json',
    )

    assert response.status_code == 403
    assert response.data == {
        'error': 'Wrong date format! YYYY-MM-DD is needed.'
    }
