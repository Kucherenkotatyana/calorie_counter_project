import pytest

from rest_framework.exceptions import ErrorDetail


@pytest.mark.django_db
def test_customer_activity_view_set_delete_data_ok(
        authenticated_client,
        activity_passed_data
):
    """
    Testing if customer can delete his activity data.
    """

    authenticated_client.post("/api/activities/", activity_passed_data)

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

    authenticated_client.post("/api/activities/", activity_passed_data)

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
    authenticated_client.post("/api/activities/", activity_passed_data)

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
