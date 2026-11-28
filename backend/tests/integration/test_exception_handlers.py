import json
import logging
import uuid

from sqlalchemy.exc import IntegrityError

from src.infrastructure.entrypoints.fastapi.exception_handlers import (
    handle_sqlalchemy_integrity_error,
)

CHANGE_WISHLIST_NAME_URL = "/wishlists/change-name/{wishlist_uuid}"
CURRENT_USER_WISHLISTS_URL = "/wishlists/"
REGISTER_URL = "/auth/register"


class TestExceptionHandlerResponses:
    def test_unknown_wishlist_returns_404(self, client):
        response = client.get(f"/wishlists/{uuid.uuid4()}")

        assert response.status_code == 404
        assert "detail" in response.json()

    def test_non_owner_modification_returns_404(
        self,
        caplog,
        client_with_populated_wishlist,
        second_user_client,
        second_user,
        populated_wishlist,
    ):
        caplog.set_level(logging.WARNING)

        url = CHANGE_WISHLIST_NAME_URL.format(wishlist_uuid=populated_wishlist.uuid)
        response = second_user_client.post(url=url, json={"new_name": "hijacked"})

        assert response.status_code == 404
        assert populated_wishlist.owner_username not in response.text
        assert str(populated_wishlist.uuid) in caplog.text
        assert second_user.username in caplog.text

    def test_invalid_token_returns_401(self, client):
        response = client.get(
            CURRENT_USER_WISHLISTS_URL,
            headers={"Authorization": "Bearer not-a-valid-token"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token"

    def test_duplicate_username_returns_409(self, client, valid_password):
        form_data = {
            "username": "sameuser",
            "email": "sameduplicate@example.com",
            "password": valid_password,
        }
        assert client.post(REGISTER_URL, data=form_data).status_code == 200

        response = client.post(REGISTER_URL, data=form_data)

        assert response.status_code == 409

    def test_invalid_username_returns_422(self, client, valid_password):
        form_data = {
            "username": "123",
            "email": "invalidusername@example.com",
            "password": valid_password,
        }
        response = client.post(REGISTER_URL, data=form_data)

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
