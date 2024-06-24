import datetime

import pytest

from src.common.service.exceptions import (
    UserNotFound,
    UserNotActive,
    PasswordVerificationError,
)


class TestUserAuthService:
    def test_generate_auth_token_and_get_username(
        self, messagebus, user_auth_service, user, valid_password
    ):
        messagebus.uow.user_repository.add(user)
        token = user_auth_service.generate_auth_token(
            username=user.username, password=valid_password
        )
        username_from_token = user_auth_service.get_username_from_token(token=token)
        assert username_from_token == user.username

    def test_generate_auth_token_wrong_username(self, user_auth_service):
        with pytest.raises(UserNotFound):
            token = user_auth_service.generate_auth_token(
                username="non-existing-user", password="password"
            )

    def test_generate_auth_token_inactive_user(
        self, messagebus, user_auth_service, deactivated_user, valid_password
    ):
        with pytest.raises(UserNotActive):
            messagebus.uow.user_repository.add(deactivated_user)
            token = user_auth_service.generate_auth_token(
                username=deactivated_user.username, password=valid_password
            )

    def test_generate_auth_token_wrong_password(
        self, messagebus, user_auth_service, user
    ):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(PasswordVerificationError):
            token = user_auth_service.generate_auth_token(
                username=user.username, password="wrong-password"
            )

    def test_get_username_from_token_expired_token(
        self, messagebus, user_auth_service, user, valid_password
    ):
        messagebus.uow.user_repository.add(user)
        token = user_auth_service.generate_auth_token(
            username=user.username,
            password=valid_password,
            exp_time=datetime.timedelta(seconds=-1),
        )
        with pytest.raises(Exception):
            user_auth_service.get_username_from_token(token=token)
