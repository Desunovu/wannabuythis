import datetime

import pytest

from src.common.service.exceptions import (
    CodeVerificationError,
    PasswordValidationError,
    PasswordVerificationError,
    UserActive,
    UserAlreadyActive,
    UserAlreadyDeactivated,
    UserExists,
    UserNotActive,
    UserNotFound,
)
from src.users.domain.commands import (
    ActivateUser,
    ActivateUserWithCode,
    ChangeEmail,
    ChangePasswordWithOldPassword,
    ChangePasswordWithoutOldPassword,
    CreateUser,
    DeactivateUser,
    GenerateAuthToken,
    ResendActivationCode,
)


class TestCreateUser:
    def test_create_user(self, messagebus, valid_password):
        messagebus.handle(
            CreateUser(
                username="testuser",
                email="testemail@example.com",
                password=valid_password,
            )
        )
        assert messagebus.uow.user_repository.get("testuser") is not None

    def test_create_user_invalid_password(self, messagebus, invalid_password):
        with pytest.raises(PasswordValidationError):
            messagebus.handle(
                CreateUser(
                    username="testuser",
                    email="testemail@example.com",
                    password=invalid_password,
                )
            )

    def test_create_user_with_existing_username(self, messagebus, user, valid_password):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(UserExists):
            messagebus.handle(
                CreateUser(
                    username=user.username,
                    email="testemail@example.com",
                    password=valid_password,
                )
            )


class TestGenerateAuthToken:
    def test_generate_auth_token_and_get_username(
        self, messagebus, user, valid_password
    ):
        messagebus.uow.user_repository.add(user)
        token = messagebus.handle(
            GenerateAuthToken(
                username=user.username,
                password=valid_password,
                token_lifetime=datetime.timedelta(minutes=1),
            )
        )
        assert token

    def test_inactive_user_allowed_to_generate_auth_token(
        self, messagebus, deactivated_user, valid_password
    ):
        messagebus.uow.user_repository.add(deactivated_user)
        command = GenerateAuthToken(
            username=deactivated_user.username,
            password=valid_password,
            token_lifetime=datetime.timedelta(minutes=1),
        )

        token = messagebus.handle(command)

        assert token

    def test_generate_auth_token_wrong_username(self, messagebus):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                GenerateAuthToken(
                    username="non-existing-user",
                    password="password",
                    token_lifetime=datetime.timedelta(minutes=1),
                )
            )

    def test_generate_auth_token_wrong_password(self, messagebus, user):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(PasswordVerificationError):
            messagebus.handle(
                GenerateAuthToken(
                    username=user.username,
                    password="wrong-password",
                    token_lifetime=datetime.timedelta(minutes=1),
                )
            )


class TestChangePassword:
    def test_change_password_by_admin(self, messagebus, user, valid_new_password):
        messagebus.uow.user_repository.add(user)
        old_password_hash = user.password_hash
        command = ChangePasswordWithoutOldPassword(
            username=user.username,
            new_password=valid_new_password,
        )

        messagebus.handle(command)

        assert user.password_hash != old_password_hash

    def test_change_password_by_user(
        self, messagebus, user, valid_password, valid_new_password
    ):
        messagebus.uow.user_repository.add(user)
        old_password_hash = user.password_hash
        command = ChangePasswordWithOldPassword(
            username=user.username,
            new_password=valid_new_password,
            old_password=valid_password,
        )

        messagebus.handle(command)

        assert user.password_hash != old_password_hash

    def test_change_password_non_existing_user(
        self, messagebus, valid_password, valid_new_password
    ):
        command_for_admin = ChangePasswordWithoutOldPassword(
            username="non-existing-user",
            new_password=valid_new_password,
        )
        command_for_user = ChangePasswordWithOldPassword(
            username="non-existing-user",
            new_password=valid_new_password,
            old_password=valid_password,
        )

        for command in [command_for_admin, command_for_user]:
            with pytest.raises(UserNotFound):
                messagebus.handle(command)

    def test_change_password_wrong_old_password(
        self, messagebus, user, invalid_password, valid_new_password
    ):
        messagebus.uow.user_repository.add(user)
        command = ChangePasswordWithOldPassword(
            username=user.username,
            new_password=valid_new_password,
            old_password=invalid_password,
        )

        with pytest.raises(PasswordVerificationError):
            messagebus.handle(command)

    def test_change_password_invalid_password(
        self, messagebus, user, invalid_password, valid_password
    ):
        messagebus.uow.user_repository.add(user)
        command_for_admin = ChangePasswordWithoutOldPassword(
            username=user.username,
            new_password=invalid_password,
        )
        command_for_user = ChangePasswordWithOldPassword(
            username=user.username,
            new_password=invalid_password,
            old_password=valid_password,
        )

        for command in [command_for_admin, command_for_user]:
            with pytest.raises(PasswordValidationError):
                messagebus.handle(command)


class TestChangeEmail:
    def test_update_email(self, messagebus, user, new_email):
        messagebus.uow.user_repository.add(user)
        messagebus.handle(ChangeEmail(username=user.username, new_email=new_email))
        assert user.email == new_email

    def test_update_email_non_existing_user(self, messagebus, new_email):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                ChangeEmail(username="non-existing-user", new_email=new_email)
            )


class TestActivateUser:
    def test_activate_user(self, messagebus, deactivated_user):
        messagebus.uow.user_repository.add(deactivated_user)
        messagebus.handle(ActivateUser(username=deactivated_user.username))
        assert deactivated_user.is_active is True

    def test_activate_non_existing_user(self, messagebus):
        with pytest.raises(UserNotFound):
            messagebus.handle(ActivateUser(username="non-existing-user"))

    def test_activate_already_active_user(self, messagebus, activated_user):
        messagebus.uow.user_repository.add(activated_user)
        with pytest.raises(UserAlreadyActive):
            messagebus.handle(ActivateUser(username=activated_user.username))


class TestActivateUserWithCode:
    @staticmethod
    def _create_code(messagebus, user):
        generator = messagebus.dependencies["activation_code_generator"]
        storage = messagebus.dependencies["activation_code_storage"]
        code = generator.create_code()
        storage.save_activation_code(username=user.username, code=code)
        return code

    def test_activate_user_with_code(
        self, messagebus, deactivated_user, valid_password
    ):
        messagebus.uow.user_repository.add(deactivated_user)
        code = self._create_code(messagebus, deactivated_user)

        messagebus.handle(
            ActivateUserWithCode(username=deactivated_user.username, code=code)
        )

        assert deactivated_user.is_active

    def test_wrong_code(self, messagebus, deactivated_user):
        messagebus.uow.user_repository.add(deactivated_user)
        code = "wrong-token"

        with pytest.raises(CodeVerificationError):
            messagebus.handle(
                ActivateUserWithCode(username=deactivated_user.username, code=code)
            )

    def test_already_active_user(self, messagebus, activated_user, valid_password):
        messagebus.uow.user_repository.add(activated_user)
        code = self._create_code(messagebus, activated_user)

        with pytest.raises(UserAlreadyActive):
            messagebus.handle(
                ActivateUserWithCode(username=activated_user.username, code=code)
            )


class TestResendActivationCode:
    def test_resend_activation_code(
        self, capsys, messagebus, deactivated_user, valid_password
    ):
        messagebus.uow.user_repository.add(deactivated_user)

        command = ResendActivationCode(
            username=deactivated_user.username, password=valid_password
        )
        messagebus.handle(command)

        captured = capsys.readouterr()
        assert deactivated_user.email in captured.out

    def test_resend_activation_code_non_existing_user(self, messagebus, valid_password):
        command = ResendActivationCode(
            username="non-existing-user", password=valid_password
        )
        with pytest.raises(UserNotFound):
            messagebus.handle(command)

    def test_resend_activation_code_wrong_password(self, messagebus, deactivated_user):
        messagebus.uow.user_repository.add(deactivated_user)

        command = ResendActivationCode(
            username=deactivated_user.username, password="wrong-password"
        )
        with pytest.raises(PasswordVerificationError):
            messagebus.handle(command)

    def test_resend_activation_code_already_active(
        self, messagebus, activated_user, valid_password
    ):
        messagebus.uow.user_repository.add(activated_user)

        command = ResendActivationCode(
            username=activated_user.username, password=valid_password
        )
        with pytest.raises(UserActive):
            messagebus.handle(command)


class TestDeactivateUser:
    def test_deactivate_user(self, messagebus, activated_user):
        messagebus.uow.user_repository.add(activated_user)
        messagebus.handle(DeactivateUser(username=activated_user.username))
        assert activated_user.is_active is False

    def test_deactivate_non_existing_user(self, messagebus):
        with pytest.raises(UserNotFound):
            messagebus.handle(DeactivateUser(username="non-existing-user"))

    def test_deactivate_non_active_user(self, messagebus, deactivated_user):
        messagebus.uow.user_repository.add(deactivated_user)
        with pytest.raises(UserAlreadyDeactivated):
            messagebus.handle(DeactivateUser(username=deactivated_user.username))
