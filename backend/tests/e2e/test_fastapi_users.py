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
    pass


class TestFastAPIUsersCommandRoutes:
    pass


class TestFastAPIUsersQueryRoutes:
    pass
