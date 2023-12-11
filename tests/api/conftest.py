import pytest

from rest_framework.test import APIClient

from users.models import Customer
from meal.models import Meal
from activity.models import CustomerActivity
from customer_profile.models import CustomerProfile


@pytest.fixture
def customer_profile_created(authenticated_client):
    customer = Customer.objects.first()

    customer_profile_data = dict(
        customer=customer,
        target=1500,
    )

    created_profile = CustomerProfile.objects.create(**customer_profile_data)
    return created_profile


@pytest.fixture
def meal_data_created(authenticated_client):
    customer = Customer.objects.first()

    product_data = dict(
        user=customer,
        date_add="2023-12-05T13:13:10Z",
        meal_type="DI",
        product_name="watermelon",
        portion_size=55.5,
        portion_calories=30.0
    )

    created_meal_data = Meal.objects.create(**product_data)
    return created_meal_data


@pytest.fixture
def meal_data_created_2(authenticated_client):
    customer = Customer.objects.first()

    product_data = dict(
        user=customer,
        date_add="2023-12-05T13:16:10Z",
        meal_type="DI",
        product_name="watermelon",
        portion_size=55.5,
        portion_calories=30.0
    )

    created_meal_data_2 = Meal.objects.create(**product_data)
    return created_meal_data_2


@pytest.fixture
def meal_data(authenticated_client):
    customer = Customer.objects.first()

    product_data = dict(
        user=customer,
        date_add="2023-10-11T13:35:10Z",
        meal_type="DI",
        product_name="watermelon",
        portion_size=55.5,
        portion_calories=30.0
    )

    return product_data


@pytest.fixture
def meal_data_2(authenticated_client):
    customer = Customer.objects.first()

    product_data = dict(
        user=customer,
        date_add="2023-10-11T13:35:10Z",
        meal_type="BR",
        product_name="coffee",
        portion_size=250,
        portion_calories=15.0
    )

    return product_data


@pytest.fixture
def meal_data_3(authenticated_client):
    customer = Customer.objects.first()

    product_data = dict(
        user=customer,
        date_add="2023-10-11T10:15:06Z",
        meal_type="BR",
        product_name="tomato",
        portion_size=100,
        portion_calories=7.0
    )

    return product_data


@pytest.fixture
def activity_passed_data():
    passed_data = dict(
        date_add="2023-08-31T17:22:10Z",
        spent_calories=25,
    )
    return passed_data


@pytest.fixture
def activity_data_created(authenticated_client):
    customer = Customer.objects.first()

    passed_data = dict(
        date_add="2023-12-05T10:22:10Z",
        spent_calories=400,
    )
    created_activity = CustomerActivity.objects.create(
        customer=customer,
        **passed_data,
    )
    return created_activity


@pytest.fixture
def authenticated_client_email():
    return 'mishaivanov@email.com'


@pytest.fixture
def authenticated_client(authenticated_client_email):
    password = '123ABC321'

    Customer.objects.create_user(
        first_name="Misha",
        last_name="Ivanov",
        email=authenticated_client_email,
        password=password,
    )

    client = APIClient()
    client.login(email=authenticated_client_email, password=password)
    return client


@pytest.fixture
def another_authenticated_client_email():
    return 'irashevchenko@email.com'


@pytest.fixture
def another_authenticated_client(another_authenticated_client_email):
    password = 'testpassword111'

    Customer.objects.create_user(
        first_name="Ira",
        last_name="Shevchenko",
        email=another_authenticated_client_email,
        password=password,
    )

    client = APIClient()
    client.login(email=another_authenticated_client_email, password=password)
    return client
