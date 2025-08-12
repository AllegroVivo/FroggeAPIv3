import pytest

from ..payloads import *
################################################################################
def assert_registration_response(response, expected_user_id):

    assert "user_id" in response, "Response should contain user ID"
    assert response["user_id"] == expected_user_id, "User ID should match the test user ID"
    assert "created_at" in response, "Response should contain creation timestamp"
    assert isinstance(response["created_at"], str), "Creation timestamp should be a string"
    assert "last_login" in response, "Response should contain last login timestamp"
    assert response["last_login"] is None, "Last login should be None for new users"

################################################################################
def test_register_user(client):
    """Test user registration endpoint."""

    res = client.post("/auth/register", json=TEST_USER_CREATE_PAYLOAD)
    assert res.status_code == 201, "Should return 201 for successful registration"
    confirmation = res.json()
    assert_registration_response(confirmation, TEST_USER_CREATE_PAYLOAD["user_id"])

################################################################################
def test_register_user_invalid_payload(client):
    """Test user registration with invalid payload."""

    res = client.post("/auth/register", json=INVALID_PAYLOAD)
    assert res.status_code == 422, "Should return 422 for invalid payload"

################################################################################
