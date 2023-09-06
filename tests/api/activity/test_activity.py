import pytest

from rest_framework.exceptions import ErrorDetail
from activity.models import CustomerActivity
from users.models import Customer

from collections import OrderedDict


@pytest.mark.django_db
def test_customer_activity_view_set_delete_data_ok(
        authenticated_client,
        activity_passed_data
):
    """
    Testing if customer can delete his activity data.
    """
    customer = Customer.objects.first()

    CustomerActivity.objects.create(
        customer=customer,
        **activity_passed_data,
    )

    response = authenticated_client.delete("/api/activities/1/")

    assert response.status_code == 204


@pytest.mark.django_db
def test_customer_activity_view_set_get_data_ok(
        authenticated_client,
        activity_passed_data
):
    """
    Testing if customer can view his activity data.
    """

    customer = Customer.objects.first()

    CustomerActivity.objects.create(
        customer=customer,
        **activity_passed_data,
    )

    response = authenticated_client.get("/api/activities/1/")
    data = response.data

    assert data["id"] == 1
    assert data["date_add"] == activity_passed_data["date_add"]
    assert data["spent_calories"] == activity_passed_data["spent_calories"]


@pytest.mark.django_db
def test_customer_activity_view_set_get_data_fail(
        authenticated_client,
        another_authenticated_client,
        activity_passed_data
):
    """
    Checking that only author can view an activity data.
    """
    customer = Customer.objects.first()

    CustomerActivity.objects.create(
        customer=customer,
        **activity_passed_data,
    )

    response = another_authenticated_client.get("/api/activities/1/")
    data = response.data

    assert data == {'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                          code='permission_denied')}


@pytest.mark.django_db
def test_customer_activity_view_set_post_data_ok(
        authenticated_client,
        activity_passed_data
):
    """
    Testing if customer can post new activity data.
    """
    response = authenticated_client.post("/api/activities/", activity_passed_data)
    data = response.data

    assert data["id"] == 1
    assert data["date_add"] == activity_passed_data["date_add"]
    assert data["spent_calories"] == activity_passed_data["spent_calories"]


@pytest.mark.django_db
def test_customer_activity_view_set_post_data_fail(
        authenticated_client,
):
    """
    Checking that only positive integers and numbers greater than 0 can be added.
    """

    wrong_data = dict(
        date_add="2023-08-31T17:22:10Z",
        spent_calories=-25,
    )

    response = authenticated_client.post("/api/activities/", wrong_data)
    data = response.data

    assert data == {'spent_calories': [ErrorDetail(string='Ensure this value is greater than or equal to 1.',
                                                   code='min_value')]}


@pytest.mark.django_db
def test_customer_activity_summarize_existing_data_ok(
        authenticated_client,
):
    """
    Testing summarizing existing data for a chosen day.
    """
    customer = Customer.objects.first()

    CustomerActivity.objects.create(
        customer=customer,
        date_add="2023-09-01T17:22:10Z",
        spent_calories=25,
    )
    CustomerActivity.objects.create(
        customer=customer,
        date_add="2023-09-01T17:25:10Z",
        spent_calories=10,
    )

    response = authenticated_client.get("/api/activities-list/?date=2023-09-01&pk=1")
    data = response.data

    assert data["total_calories"] == 35
    assert data["records"] == [
        OrderedDict([('id', 1), ('date_add', '2023-09-01T17:22:10Z'), ('spent_calories', 25)]),
        OrderedDict([('id', 2), ('date_add', '2023-09-01T17:25:10Z'), ('spent_calories', 10)])
    ]


@pytest.mark.django_db
def test_customer_activity_summarize_existing_data_fail(
        authenticated_client,
):
    """
    Testing if Customer gets a proper error if Customer has no existing data for a chosen day.
    """

    response = authenticated_client.get("/api/activities-list/?date=2023-09-01&pk=1")
    data = response.data

    assert data == {"error": "No added activities for the chosen date"}
    assert response.status_code == 404
