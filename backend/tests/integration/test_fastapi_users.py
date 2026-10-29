from src.modules.users.application.refresh_token_service import RefreshTokenService
from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.activation_codes.activation_code_generator import (
    ActivationCodeGenerator,
)
from tests.integration.helpers import app_uow

ADMIN_USERS_URL = "/admin/users"
AUTH_REGISTER_URL = "/auth/register"
AUTH_LOGIN_URL = "/auth/login"
AUTH_REFRESH_URL = "/auth/refresh"
AUTH_LOGOUT_URL = "/auth/logout"
AUTH_ACTIVATE_URL = "/auth/activate"
AUTH_RESEND_ACTIVATION_URL = "/auth/resend-activation"
CHANGE_EMAIL_URL = "/users/me/email"
CHANGE_PASSWORD_URL = "/users/me/password"
GET_CURRENT_USER_URL = "/users/me"
GET_USERS_URL = "/users"


class TestFastAPIUsersAdminRoutes:
    def test_activate_user(
        self, admin_client_contains_deactivated_user, deactivated_user
    ):
        url = f"{ADMIN_USERS_URL}/{deactivated_user.username}/activate"
        response = admin_client_contains_deactivated_user.patch(url)
        assert response.status_code == 200

    def test_deactivate_user(
        self, admin_client_contains_activated_user, activated_user
    ):
        url = f"{ADMIN_USERS_URL}/{activated_user.username}/deactivate"
        response = admin_client_contains_activated_user.patch(url=url)
        assert response.status_code == 200

    def test_change_password(
        self, admin_client_contains_activated_user, activated_user, valid_new_password
    ):
        url = f"{ADMIN_USERS_URL}/{activated_user.username}/password"
        body = {"new_password": valid_new_password}
        response = admin_client_contains_activated_user.patch(url=url, json=body)
        assert response.status_code == 200

    def test_change_email(
        self, admin_client_contains_activated_user, activated_user, new_email
    ):
        url = f"{ADMIN_USERS_URL}/{activated_user.username}/email"
        body = {"new_email": new_email}
        response = admin_client_contains_activated_user.patch(url=url, json=body)
        assert response.status_code == 200


class TestFastAPIUsersAuthRoutes:
    @staticmethod
    def _create_code(client, user):
        container = client.app.state.dishka_container
        generator = container.get(ActivationCodeGenerator)
        storage = container.get(ActivationCodeStorage)
        code = generator.create_code()
        storage.save_activation_code(username=user.username, code=code)
        return code

    def test_register(self, client, valid_password):
        form_data = {
            "username": "username",
            "email": "username@example.com",
            "password": valid_password,
        }
        response = client.post(url=AUTH_REGISTER_URL, data=form_data)
        assert response.status_code == 200

    def test_register_invalid_email(self, client, valid_password):
        form_data = {
            "username": "username",
            "email": "not-an-email",
            "password": valid_password,
        }
        response = client.post(url=AUTH_REGISTER_URL, data=form_data)
        assert response.status_code == 422

    def test_login(self, user_client, user, valid_password):
        form_data = {"username": user.username, "password": valid_password}
        response = user_client.post(url=AUTH_LOGIN_URL, data=form_data)
        assert response.status_code == 200
        token_pair = response.json()
        assert token_pair["access_token"]
        assert token_pair["refresh_token"]
        assert token_pair["token_type"] == "bearer"

        with app_uow(user_client) as uow:
            stored_refresh_token = uow.refresh_token_repository.get_by_hash(
                RefreshTokenService.hash_token(token_pair["refresh_token"])
            )

        assert stored_refresh_token is not None
        assert stored_refresh_token.username == user.username

    def test_refresh(self, client_with_user, user, valid_password):
        form_data = {"username": user.username, "password": valid_password}
        login_response = client_with_user.post(url=AUTH_LOGIN_URL, data=form_data)
        old_token_pair = login_response.json()

        response = client_with_user.post(
            url=AUTH_REFRESH_URL,
            json={"refresh_token": old_token_pair["refresh_token"]},
        )

        assert response.status_code == 200
        new_token_pair = response.json()
        assert new_token_pair["access_token"]
        assert new_token_pair["refresh_token"] != old_token_pair["refresh_token"]

        reuse_response = client_with_user.post(
            url=AUTH_REFRESH_URL,
            json={"refresh_token": old_token_pair["refresh_token"]},
        )
        assert reuse_response.status_code == 401

        second_response = client_with_user.post(
            url=AUTH_REFRESH_URL,
            json={"refresh_token": new_token_pair["refresh_token"]},
        )
        assert second_response.status_code == 200

    def test_logout(self, client_with_user, user, valid_password):
        form_data = {"username": user.username, "password": valid_password}
        login_response = client_with_user.post(url=AUTH_LOGIN_URL, data=form_data)
        token_pair = login_response.json()

        logout_response = client_with_user.post(
            url=AUTH_LOGOUT_URL,
            json={"refresh_token": token_pair["refresh_token"]},
        )

        assert logout_response.status_code == 200
        refresh_response = client_with_user.post(
            url=AUTH_REFRESH_URL,
            json={"refresh_token": token_pair["refresh_token"]},
        )
        assert refresh_response.status_code == 401

    def test_login_deactivated_user_rejected(
        self, client_with_deactivated_user, deactivated_user, valid_password
    ):
        form_data = {
            "username": deactivated_user.username,
            "password": valid_password,
        }
        response = client_with_deactivated_user.post(url=AUTH_LOGIN_URL, data=form_data)
        assert response.status_code == 403

    def test_deactivated_user_rejected_on_protected_route(
        self, client_with_deactivated_user_token
    ):
        response = client_with_deactivated_user_token.get(GET_CURRENT_USER_URL)
        assert response.status_code == 403

    def test_activate(self, client_with_deactivated_user, deactivated_user):
        code = self._create_code(
            client=client_with_deactivated_user,
            user=deactivated_user,
        )
        body = {"username": deactivated_user.username, "code": code}
        response = client_with_deactivated_user.post(url=AUTH_ACTIVATE_URL, json=body)
        assert response.status_code == 200

    def test_activate_with_wrong_code(
        self, client_with_deactivated_user, deactivated_user
    ):
        body = {"username": deactivated_user.username, "code": "00000000"}
        response = client_with_deactivated_user.post(url=AUTH_ACTIVATE_URL, json=body)
        assert response.status_code == 401

    def test_activation_code_is_single_use(
        self, client_with_deactivated_user, deactivated_user
    ):
        code = self._create_code(
            client=client_with_deactivated_user,
            user=deactivated_user,
        )
        body = {"username": deactivated_user.username, "code": code}
        first = client_with_deactivated_user.post(url=AUTH_ACTIVATE_URL, json=body)
        second = client_with_deactivated_user.post(url=AUTH_ACTIVATE_URL, json=body)
        assert first.status_code == 200
        assert second.status_code == 401

    def test_resend_activation_link(
        self, client_with_deactivated_user, deactivated_user, valid_password
    ):
        form_data = {"username": deactivated_user.username, "password": valid_password}
        response = client_with_deactivated_user.post(
            url=AUTH_RESEND_ACTIVATION_URL, data=form_data
        )
        assert response.status_code == 200


class TestFastAPIUsersCommandRoutes:
    def test_change_password(
        self, user_client, user, valid_password, valid_new_password
    ):
        body = {
            "username": user.username,
            "old_password": valid_password,
            "new_password": valid_new_password,
        }
        response = user_client.patch(url=CHANGE_PASSWORD_URL, json=body)
        assert response.status_code == 200

    def test_change_email(self, user_client, user, new_email):
        body = {"username": user.username, "new_email": new_email}
        response = user_client.patch(url=CHANGE_EMAIL_URL, json=body)
        assert response.status_code == 200


class TestFastAPIUsersQueryRoutes:
    def test_get_me(self, user_client, user):
        response = user_client.get(GET_CURRENT_USER_URL)
        assert response.status_code == 200
        assert response.json()["username"] == user.username

    def test_get_users(self, user_client):
        response = user_client.get(GET_USERS_URL)
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_get_user(self, client_with_user, user):
        url = f"{GET_USERS_URL}/{user.username}"
        response = client_with_user.get(url)
        assert response.status_code == 200
        assert response.json()["username"] == user.username
