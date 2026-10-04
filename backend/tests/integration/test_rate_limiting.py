from fastapi.testclient import TestClient

from tests.integration.conftest import (
    add_authorization_header_to_client,
    add_user_to_db,
)

LOGIN_LIMIT = 10  # mirrors the limit on /auth/login
READ_LIMIT = 60  # mirrors the limit on /users/ and /users/{username}
ME_LIMIT = 120  # mirrors the limit on /users/me


class TestRateLimiting:
    def test_login_is_rate_limited(self, client: TestClient):
        codes = [
            client.post(
                "/auth/login", data={"username": "nobody", "password": "secret"}
            ).status_code
            for _ in range(LOGIN_LIMIT + 1)
        ]

        assert codes[-1] == 429
        assert set(codes[:-1]) == {404}

    def test_user_list_is_rate_limited(self, client: TestClient, user):
        add_user_to_db(client, user)

        codes = [client.get("/users/").status_code for _ in range(READ_LIMIT + 1)]

        assert codes[-1] == 429
        assert set(codes[:-1]) == {200}

    def test_user_by_username_is_rate_limited(self, client: TestClient, user):
        add_user_to_db(client, user)

        codes = [
            client.get(f"/users/{user.username}").status_code
            for _ in range(READ_LIMIT + 1)
        ]

        assert codes[-1] == 429
        assert set(codes[:-1]) == {200}

    def test_current_user_route_is_rate_limited(self, user_client: TestClient):
        codes = [user_client.get("/users/me").status_code for _ in range(ME_LIMIT + 1)]

        assert set(codes[:-1]) == {200}
        assert codes[-1] == 429

    def test_limit_is_not_shared_between_users(
        self, client: TestClient, user, second_user
    ):
        add_user_to_db(client, user)
        add_user_to_db(client, second_user)

        codes = []
        for _ in range(ME_LIMIT):
            for current_user in (user, second_user):
                add_authorization_header_to_client(client, current_user)
                codes.append(client.get("/users/me").status_code)

        assert set(codes) == {200}
