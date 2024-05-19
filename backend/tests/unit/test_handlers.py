import pytest

from src.domain.user.commands import CreateUser, ChangePassword
from src.service_layer.user_handlers import (
    UserNotFound,
    UserExists,
    InvalidOldPassword,
    InvalidPassword,
)


class TestCreateUser:
    def test_create_new_user(self, messagebus, valid_password):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_password)
        )

        assert messagebus.uow.user_repository.get("testuser") is not None

    def test_create_existing_user(self, messagebus, valid_password):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_password)
        )

        with pytest.raises(UserExists):
            messagebus.handle(
                CreateUser("testuser", "testemail@example.com", valid_password)
            )


class TestChangePassword:
    def test_change_password_by_admin(
        self, messagebus, valid_password, valid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        user = messagebus.uow.user_repository.get("testuser")
        old_password_hash = user.password_hash
        messagebus.handle(
            ChangePassword("testuser", valid_password, called_by_admin=True)
        )

        assert user.password_hash != old_password_hash

    def test_change_password_by_user(
        self, messagebus, valid_password, valid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        user = messagebus.uow.user_repository.get("testuser")
        old_password_hash = user.password_hash
        messagebus.handle(
            ChangePassword("testuser", valid_password, valid_old_password)
        )

        assert user.password_hash != old_password_hash

    def test_change_password_non_existing_user(self, messagebus, valid_password):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                ChangePassword("testuser", valid_password, valid_password)
            )

    def test_change_password_invalid_old_password(
        self, messagebus, valid_password, valid_old_password, invalid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        with pytest.raises(InvalidOldPassword):
            messagebus.handle(
                ChangePassword("testuser", valid_password, invalid_old_password)
            )

    def test_change_password_invalid_password(
        self, messagebus, invalid_password, valid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        with pytest.raises(InvalidPassword):
            messagebus.handle(
                ChangePassword("testuser", invalid_password, valid_old_password)
            )
