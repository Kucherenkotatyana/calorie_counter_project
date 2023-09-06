import pytest

from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail

from users.models import Customer


client = APIClient()


@pytest.mark.django_db
def test_customer_register_ok():
    passed_data = dict(
        first_name="Misha",
        last_name="Ivanov",
        email="mishaivanov@email.com",
        password="123ABC321"
    )

    response = client.post("/api/customer/register/", passed_data)
    data = response.data

    customer = Customer.objects.first()

    assert data["first_name"] == customer.first_name
    assert data["last_name"] == customer.last_name
    assert data["email"] == customer.email

    assert data["first_name"] == passed_data["first_name"]
    assert data["last_name"] == passed_data["last_name"]
    assert data["email"] == passed_data["email"]
    assert "password" not in data

    assert response.status_code == 201


@pytest.mark.django_db
def test_customer_register_fail():
    passed_data = dict(
        first_name="Misha",
        last_name="Ivanov",
        password="123ABC321"
    )

    response = client.post("/api/customer/register/", passed_data)
    data = response.data

    assert data == {'email': [ErrorDetail(string='This field is required.', code='required')]}
    assert response.status_code == 400


@pytest.mark.django_db
def test_customer_show_details_ok(
        authenticated_client,
        authenticated_client_email,
):
    response = authenticated_client.get("/api/customer/show-details/")

    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": authenticated_client_email,
        "first_name": "Misha",
        "last_name": "Ivanov",
    }
