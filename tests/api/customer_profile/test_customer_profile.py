import pytest

from rest_framework.exceptions import ErrorDetail
from rest_framework import serializers

from customer_profile.models import CustomerProfile
from customer_profile.serializers import (
    CustomerProfileSerializer,
    CustomerProfileUpdateSerializer,
)

from users.models import Customer


@pytest.mark.django_db
def test_customer_profile_view_post_ok(
        authenticated_client,
):
    """
    Testing if the customer can create a profile.
    """
    response = authenticated_client.post(
        f"/api/customer-profile/1/",
        {"target": 1500},
        format='json',
    )

    assert response.status_code == 201
    assert response.data == {'id': 1, 'target': 1500}

@pytest.mark.django_db
def test_customer_profile_view_post_nonexistent_customer(
        authenticated_client,
):
    """
    Testing if the view returns a proper error while passing nonexistent
    customer id.
    """
    response = authenticated_client.post(
        f"/api/customer-profile/3/",
        {"target": 1500},
        format='json',
    )

    assert response.status_code == 404
    assert response.data == {
        'detail': ErrorDetail(string='Not found.', code='not_found')
    }


@pytest.mark.django_db
def test_customer_profile_view_post_forbidden(
        authenticated_client,
        another_authenticated_client
):
    """
    Testing if only current customer can create his own profile.
    """
    response = authenticated_client.post(
        f"/api/customer-profile/2/",
    )

    assert response.status_code == 403
    assert response.data == {'error': 'Action not allowed.'}


@pytest.mark.django_db
def test_customer_profile_view_post_pass_invalid_data(
        authenticated_client,
):
    """
    Testing if the view returns a proper error if invalid data
    was passed.
    """
    response = authenticated_client.post(
        f"/api/customer-profile/1/",
        {"test": 1500},
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        'target': [
            ErrorDetail(string='This field is required.', code='required')
        ]
    }


@pytest.mark.django_db
def test_customer_profile_view_post_value_validator(
        authenticated_client,
):
    """
    Testing if the MinValueValidator in the model works properly.
    """
    response = authenticated_client.post(
        f"/api/customer-profile/1/",
        {"target": 0},
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        'target': [
            ErrorDetail(
                string='Ensure this value is greater than or equal to 1.',
                code='min_value'
            )
        ]
    }


@pytest.mark.django_db
def test_customer_profile_view_post_second_time(
        authenticated_client,
):
    """
    Testing if the customer can't post data again after profile
    was created.
    """
    customer = Customer.objects.first()
    customer_profile_data = dict(
        customer=customer,
        target=1500,
    )
    CustomerProfile.objects.create(**customer_profile_data)

    response = authenticated_client.post(
        f"/api/customer-profile/1/",
        {"target": 2000},
        format='json',
    )

    assert response.status_code == 400
    assert response.data == {
        'non_field_errors': [
            ErrorDetail(string='Customer already has a target', code='invalid')
        ]
    }


@pytest.mark.django_db
def test_customer_profile_view_get_ok(
        authenticated_client,
        customer_profile_created,
):
    """
    Testing if the customer can get his target.
    """
    response = authenticated_client.get(
        f"/api/customer-profile/1/",
    )

    assert response.status_code == 200
    assert response.data == {'id': 1, 'target': 1500}


@pytest.mark.django_db
def test_customer_profile_view_get_not_found(
        authenticated_client,
):
    """
    Testing if the customer gets NotFound if he doesn't already
    have a target.
    """
    response = authenticated_client.get(
        f"/api/customer-profile/1/",
    )

    assert response.status_code == 404
    assert response.data == {
        'No CustomerProfile matches the given query. '
        'Check if you passed a valid customer id.'
    }


@pytest.mark.django_db
def test_customer_profile_view_get_nonexistent_customer(
        authenticated_client,
):
    """
    Testing if only the customer get NotFound trying to access
    non-existent profile.
    """
    response = authenticated_client.get(
        f"/api/customer-profile/2/",
    )

    assert response.status_code == 404
    assert response.data == {
        'detail': ErrorDetail(string='Not found.', code='not_found')
    }


@pytest.mark.django_db
def test_customer_profile_view_patch_ok(
        authenticated_client,
        customer_profile_created,
):
    """
    Testing if the customer can change the target in his profile.
    """
    response = authenticated_client.patch(
        f"/api/customer-profile/1/",
        {"target": 1234},
        format='json',
    )
    assert response.status_code == 200
    assert response.data == {'id': 1, 'target': 1234}


@pytest.mark.django_db
def test_customer_profile_view_patch_not_found(
        authenticated_client,
):
    """
    Testing if the customer gets a proper error trying to patch
    non-existent target.
    """
    response = authenticated_client.patch(
        f"/api/customer-profile/1/",
        {"target": 1234},
        format='json',
    )
    assert response.status_code == 404
    assert response.data == {
        'No CustomerProfile matches the given query. '
        'You can change only existing profile!'
    }


@pytest.mark.django_db
def test_customer_profile_view_patch_forbidden(
        authenticated_client,
        another_authenticated_client,
):
    """
    Testing if the customer can't change other profile.
    """
    response = authenticated_client.patch(
        f"/api/customer-profile/2/",
    )
    assert response.status_code == 403
    assert response.data == {'error': 'Action not allowed.'}


@pytest.mark.django_db
def test_customer_profile_view_patch_invalid_instance_name(
        authenticated_client,
        customer_profile_created,
):
    """
    Testing if the customer gets BadRequest passing invalid instance.
    """
    response = authenticated_client.patch(
        f"/api/customer-profile/1/",
        {"test": 100},
        format='json',
    )
    assert response.status_code == 400
    assert response.data == {
        'Invalid data was passed to CustomerProfileUpdateSerializer. '
        'You need to pass a valid integer to update your target!'
    }


@pytest.mark.django_db
def test_customer_profile_view_patch_invalid_instance_data(
        authenticated_client,
        customer_profile_created,
):
    """
    Testing if the customer gets BadRequest passing invalid
    instance data.
    """
    response = authenticated_client.patch(
        f"/api/customer-profile/1/",
        {"target": 0},
        format='json',
    )
    assert response.status_code == 400
    assert response.data == {
        "{'target': ["
        "ErrorDetail(string='Ensure this value is greater than or equal to 1."
        "', code='min_value')]}. You need to pass a valid integer to update "
        "your target!"}


@pytest.mark.django_db
def test_customer_profile_view_patch_invalid_no_passed_data(
        authenticated_client,
        customer_profile_created,
):
    """
    Testing if the customer gets BadRequest passing no data.
    """
    response = authenticated_client.patch(
        f"/api/customer-profile/1/",
    )
    assert response.status_code == 400
    assert response.data == {
        'Invalid data was passed to CustomerProfileUpdateSerializer. '
        'You need to pass a valid integer to update your target!'
    }


@pytest.mark.django_db
def test_customer_profile_view_delete_ok(
        authenticated_client,
        customer_profile_created,
):
    """
    Testing if the customer can delete his profile.
    """
    response = authenticated_client.delete(
        f"/api/customer-profile/1/",
    )
    assert response.status_code == 204
    assert response.data == {'Deleted.'}


@pytest.mark.django_db
def test_customer_profile_view_delete_forbidden(
        authenticated_client,
        another_authenticated_client,
        customer_profile_created,
):
    """
    Testing if the customer can't delete other customer's profile.
    """
    response = another_authenticated_client.delete(
        f"/api/customer-profile/1/",
    )
    assert response.status_code == 403
    assert response.data == {'error': 'Action not allowed.'}


@pytest.mark.django_db
def test_customer_profile_view_delete_not_found(
        authenticated_client,
):
    """
    Testing if the customer gets NotFound trying to delete
    non-existent profile.
    """
    response = authenticated_client.delete(
        f"/api/customer-profile/1/",
    )
    assert response.status_code == 404
    assert response.data == {
        'No CustomerProfile matches the given query. '
        'No such profile data was found!'
    }
