class TestFastAPIUsersAdminRoutes:
    def test_activate_user(
        self, admin_client_contains_deactivated_user, deactivated_user
    ):
        url = "/admin/users/activate"
        body = {"username": deactivated_user.username}
        response = admin_client_contains_deactivated_user.post(url=url, json=body)
        assert response.status_code == 200

    def test_deactivate_user(
        self, admin_client_contains_activated_user, activated_user
    ):
        url = "/admin/users/deactivate"
        body = {"username": activated_user.username}
        response = admin_client_contains_activated_user.post(url=url, json=body)
        assert response.status_code == 200

    def test_change_password(
        self, admin_client_contains_activated_user, activated_user, valid_new_password
    ):
        url = "/admin/users/change-password"
        body = {"username": activated_user.username, "new_password": valid_new_password}
        response = admin_client_contains_activated_user.post(url=url, json=body)
        assert response.status_code == 200

    def test_change_email(
        self, admin_client_contains_activated_user, activated_user, new_email
    ):
        url = "/admin/users/change-email"
        body = {"username": activated_user.username, "new_email": new_email}
        response = admin_client_contains_activated_user.post(url=url, json=body)
        assert response.status_code == 200

    def test_add_role(
        self, admin_client_contains_user_and_default_role, user, roles_default_role
    ):
        url = "/admin/users/add-role"
        body = {"username": user.username, "role_name": roles_default_role.name}
        response = admin_client_contains_user_and_default_role.post(url=url, json=body)
        assert response.status_code == 200

    def test_remove_role(
        self,
        admin_client_contains_user_with_default_role,
        user,
        roles_default_role,
    ):
        url = "/admin/users/remove-role"
        body = {"username": user.username, "role_name": roles_default_role.name}
        response = admin_client_contains_user_with_default_role.post(url=url, json=body)
        assert response.status_code == 200


class TestFastAPIUsersAuthRoutes:
    def test_register(self, client, valid_password):
        url = "/register"
        body = {"username": "username", "email": "email", "password": valid_password}
        response = client.post(url, json=body)
        assert response.status_code == 200

    def test_activate_by_token(self, client_with_deactivated_user, deactivated_user):
        token_manager = client_with_deactivated_user.app.state.dependencies[
            "token_manager"
        ]
        token = token_manager.generate_token(username=deactivated_user.username)
        url = f"/activate/{token}"
        response = client_with_deactivated_user.get(url)
        assert response.status_code == 200

    def test_resend_activation_link(
        self, client_with_deactivated_user, deactivated_user, valid_password
    ):
        url = "/activate/resend-activation-link"
        body = {"username": deactivated_user.username, "password": valid_password}
        response = client_with_deactivated_user.post(url, json=body)
        assert response.status_code == 200

    def test_login(self, user_client, user, valid_password):
        url = "/login"
        form_data = {"username": user.username, "password": valid_password}
        response = user_client.post(url, data=form_data)
        assert response.status_code == 200


class TestFastAPIUsersCommandRoutes:
    pass


class TestFastAPIUsersQueryRoutes:
    pass
