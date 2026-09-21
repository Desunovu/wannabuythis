import json
import logging
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from src.infrastructure.entrypoints.fastapi.exception_handlers import (
    handle_sqlalchemy_integrity_error,
)
from tests.integration.conftest import (
    add_authorization_header_to_client,
    add_user_to_db,
    add_wishlist_to_db,
)

CHANGE_WISHLIST_NAME_URL = "/wishlists/change-name/{wishlist_uuid}"
CURRENT_USER_WISHLISTS_URL = "/wishlists/"
REGISTER_URL = "/auth/register"


@pytest.fixture
def error_client(fastapi_app_with_test_database) -> TestClient:
    with TestClient(
        fastapi_app_with_test_database, raise_server_exceptions=False
    ) as test_client:
        yield test_client


class TestExceptionHandlerResponses:
    def test_unknown_wishlist_returns_404(self, error_client):
        response = error_client.get(f"/wishlists/{uuid.uuid4()}")

        assert response.status_code == 404
        assert "detail" in response.json()

    def test_non_owner_modification_returns_403(
        self, error_client, admin_user, user, wishlist
    ):
        add_user_to_db(error_client, admin_user)
        add_user_to_db(error_client, user)
        add_wishlist_to_db(error_client, wishlist)
        add_authorization_header_to_client(error_client, admin_user)

        url = CHANGE_WISHLIST_NAME_URL.format(wishlist_uuid=wishlist.uuid)
        response = error_client.post(url=url, json={"new_name": "hijacked"})

        assert response.status_code == 403

    def test_invalid_token_returns_401(self, error_client):
        response = error_client.get(
            CURRENT_USER_WISHLISTS_URL,
            headers={"Authorization": "Bearer not-a-valid-token"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

    def test_duplicate_username_returns_409(self, error_client, valid_password):
        form_data = {
            "username": "sameuser",
            "email": "sameduplicate@example.com",
            "password": valid_password,
        }
        assert error_client.post(REGISTER_URL, data=form_data).status_code == 200

        response = error_client.post(REGISTER_URL, data=form_data)

        assert response.status_code == 409

    def test_invalid_username_returns_422(self, error_client, valid_password):
        form_data = {
            "username": "123",
            "email": "invalidusername@example.com",
            "password": valid_password,
        }
        response = error_client.post(REGISTER_URL, data=form_data)

        assert response.status_code == 422
        assert "at least one letter" in response.json()["detail"]


class TestIntegrityErrorHandler:
    def test_hides_driver_text_and_logs_it(self, caplog):
        driver_text = (
            "duplicate key value violates unique constraint 'users_username_key'\n"
            "DETAIL: Key (username)=(testuser) already exists."
        )
        exception = IntegrityError("INSERT INTO users ...", {}, Exception(driver_text))
        caplog.set_level(logging.WARNING)

        response = handle_sqlalchemy_integrity_error(request=None, exception=exception)

        assert response.status_code == 409
        assert json.loads(response.body) == {"detail": "Data conflict"}
        assert driver_text not in response.body.decode()
        assert "users_username_key" in caplog.text
