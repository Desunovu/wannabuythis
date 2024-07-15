ADMIN_ACTIVATE_URL = "/admin/users/activate"
ADMIN_DEACTIVATE_URL = "/admin/users/deactivate"
ADMIN_CHANGE_PASSWORD_URL = "/admin/users/change-password"
ADMIN_CHANGE_EMAIL_URL = "/admin/users/change-email"
CHANGE_EMAIL_URL = "/users/change-email"
CHANGE_PASSWORD_URL = "/users/change-password"
REGISTER_URL = "/register"
ACTIVATE_URL = "/activate"
RESEND_ACTIVATION_URL = "/resend-activation"
LOGIN_URL = "/login"
GET_CURRENT_USER_URL = "/users/me"
GET_USER_URL = "/users"


class TestFastAPIUsersAdminRoutes:
    def test_activate_user(
        self, admin_client_contains_deactivated_user, deactivated_user
    ):
        body = {"username": deactivated_user.username}
        response = admin_client_contains_deactivated_user.post(
            url=ADMIN_ACTIVATE_URL, json=body
        )
        assert response.status_code == 200

    def test_deactivate_user(
        self, admin_client_contains_activated_user, activated_user
    ):
        body = {"username": activated_user.username}
        response = admin_client_contains_activated_user.post(
            url=ADMIN_DEACTIVATE_URL, json=body
        )
        assert response.status_code == 200

    def test_change_password(
        self, admin_client_contains_activated_user, activated_user, valid_new_password
    ):
        body = {"username": activated_user.username, "new_password": valid_new_password}
        response = admin_client_contains_activated_user.post(
            url=ADMIN_CHANGE_PASSWORD_URL, json=body
        )
        assert response.status_code == 200

    def test_change_email(
        self, admin_client_contains_activated_user, activated_user, new_email
    ):
        body = {"username": activated_user.username, "new_email": new_email}
        response = admin_client_contains_activated_user.post(
            url=ADMIN_CHANGE_EMAIL_URL, json=body
        )
        assert response.status_code == 200


class TestFastAPIUsersAuthRoutes:
    @staticmethod
    def _create_code(client, user):
        generator = client.app.state.messagebus.dependencies[
            "activation_code_generator"
        ]
        storage = client.app.state.messagebus.dependencies["activation_code_storage"]
        code = generator.create_code()
        storage.save_activation_code(username=user.username, code=code)
        return code

    def test_register(self, client, valid_password):
        body = {"username": "username", "email": "email", "password": valid_password}
        response = client.post(url=REGISTER_URL, json=body)
        assert response.status_code == 200

    def test_activate(self, client_with_deactivated_user, deactivated_user):
        code = self._create_code(
            client=client_with_deactivated_user,
            user=deactivated_user,
        )
        body = {"username": deactivated_user.username, "code": code}
        response = client_with_deactivated_user.post(url=ACTIVATE_URL, json=body)
        assert response.status_code == 200

    def test_resend_activation_link(
        self, client_with_deactivated_user, deactivated_user, valid_password
    ):
        form_data = {"username": deactivated_user.username, "password": valid_password}
        response = client_with_deactivated_user.post(
            RESEND_ACTIVATION_URL, data=form_data
        )
        assert response.status_code == 200

    def test_login(self, user_client, user, valid_password):
        form_data = {"username": user.username, "password": valid_password}
        response = user_client.post(url=LOGIN_URL, data=form_data)
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
        response = user_client.post(url=CHANGE_PASSWORD_URL, json=body)
        assert response.status_code == 200

    def test_change_email(self, user_client, user, new_email):
        body = {"username": user.username, "new_email": new_email}
        response = user_client.post(url=CHANGE_EMAIL_URL, json=body)
        assert response.status_code == 200


class TestFastAPIUsersQueryRoutes:
    def test_get_me(self, user_client, user):
        response = user_client.get(GET_CURRENT_USER_URL)
        assert response.status_code == 200
        assert response.json()["username"] == user.username

    def test_get_user(self, client_with_user, user):
        url = f"{GET_USER_URL}/{user.username}"
        response = client_with_user.get(url)
        assert response.status_code == 200
