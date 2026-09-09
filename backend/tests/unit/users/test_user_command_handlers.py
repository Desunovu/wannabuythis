import datetime
import logging

import pytest

from src.modules.users.domain.commands import (
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
from src.shared.application.exceptions import (
    CodeVerificationError,
    PasswordValidationError,
    PasswordVerificationError,
    UserActive,
    UserAlreadyActive,
    UserAlreadyDeactivated,
    UserExists,
    UserInvalidName,
    UserNotFound,
)


class TestCreateUser:
    def test_create_user(self, mediator, uow, valid_password):
        mediator.handle(
            CreateUser(
                username="testuser",
                email="testemail@example.com",
                password=valid_password,
            )
        )
        assert uow.user_repository.get("testuser") is not None

    def test_create_user_invalid_password(self, mediator, invalid_password):
        with pytest.raises(PasswordValidationError):
            mediator.handle(
                CreateUser(
                    username="testuser",
                    email="testemail@example.com",
                    password=invalid_password,
                )
            )

    def test_create_user_with_existing_username(
        self, mediator, uow, user, valid_password
    ):
        uow.user_repository.add(user)
        with pytest.raises(UserExists):
            mediator.handle(
                CreateUser(
                    username=user.username,
                    email="testemail@example.com",
                    password=valid_password,
                )
            )

    @pytest.mark.parametrize(
        "forbidden_username",
        [
            "",
            "admin",
            "123",
            "a" * 51,
            "a b",
        ],
    )
    def test_create_user_invalid_username(
        self, mediator, forbidden_username, valid_password
    ):
        with pytest.raises(UserInvalidName):
            mediator.handle(
                CreateUser(
                    username=forbidden_username,
                    email="testemail@example.com",
                    password=valid_password,
                )
            )


class TestGenerateAuthToken:
    def test_generate_auth_token_and_get_username(
        self, mediator, uow, user, valid_password
    ):
        uow.user_repository.add(user)
        token = mediator.handle(
            GenerateAuthToken(
                username=user.username,
                password=valid_password,
                token_lifetime=datetime.timedelta(minutes=1),
            )
        )
        assert token

    def test_inactive_user_allowed_to_generate_auth_token(
        self, mediator, uow, deactivated_user, valid_password
    ):
        uow.user_repository.add(deactivated_user)
        command = GenerateAuthToken(
            username=deactivated_user.username,
            password=valid_password,
            token_lifetime=datetime.timedelta(minutes=1),
        )

        token = mediator.handle(command)

        assert token

    def test_generate_auth_token_wrong_username(self, mediator):
        with pytest.raises(UserNotFound):
            mediator.handle(
                GenerateAuthToken(
                    username="non-existing-user",
                    password="password",
                    token_lifetime=datetime.timedelta(minutes=1),
                )
            )

    def test_generate_auth_token_wrong_password(self, mediator, uow, user):
        uow.user_repository.add(user)
        with pytest.raises(PasswordVerificationError):
            mediator.handle(
                GenerateAuthToken(
                    username=user.username,
                    password="wrong-password",
                    token_lifetime=datetime.timedelta(minutes=1),
                )
            )


class TestChangePassword:
    def test_change_password_by_admin(self, mediator, uow, user, valid_new_password):
        uow.user_repository.add(user)
        old_password_hash = user.password_hash
        command = ChangePasswordWithoutOldPassword(
            username=user.username,
            new_password=valid_new_password,
        )

        mediator.handle(command)

        assert user.password_hash != old_password_hash

    def test_change_password_by_user(
        self, mediator, uow, user, valid_password, valid_new_password
    ):
        uow.user_repository.add(user)
        old_password_hash = user.password_hash
        command = ChangePasswordWithOldPassword(
            username=user.username,
            new_password=valid_new_password,
            old_password=valid_password,
        )

        mediator.handle(command)

        assert user.password_hash != old_password_hash

    def test_change_password_non_existing_user(
        self, mediator, valid_password, valid_new_password
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
                mediator.handle(command)

    def test_change_password_wrong_old_password(
        self, mediator, uow, user, invalid_password, valid_new_password
    ):
        uow.user_repository.add(user)
        command = ChangePasswordWithOldPassword(
            username=user.username,
            new_password=valid_new_password,
            old_password=invalid_password,
        )

        with pytest.raises(PasswordVerificationError):
            mediator.handle(command)

    def test_change_password_invalid_password(
        self, mediator, uow, user, invalid_password, valid_password
    ):
        uow.user_repository.add(user)
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
                mediator.handle(command)


class TestChangeEmail:
    def test_update_email(self, mediator, uow, user, new_email):
        uow.user_repository.add(user)
        mediator.handle(ChangeEmail(username=user.username, new_email=new_email))
        assert user.email == new_email

    def test_update_email_non_existing_user(self, mediator, new_email):
        with pytest.raises(UserNotFound):
            mediator.handle(
                ChangeEmail(username="non-existing-user", new_email=new_email)
            )


class TestActivateUser:
    def test_activate_user(self, mediator, uow, deactivated_user):
        uow.user_repository.add(deactivated_user)
        mediator.handle(ActivateUser(username=deactivated_user.username))
        assert deactivated_user.is_active is True

    def test_activate_non_existing_user(self, mediator):
        with pytest.raises(UserNotFound):
            mediator.handle(ActivateUser(username="non-existing-user"))

    def test_activate_already_active_user(self, mediator, uow, activated_user):
        uow.user_repository.add(activated_user)
        with pytest.raises(UserAlreadyActive):
            mediator.handle(ActivateUser(username=activated_user.username))


class TestActivateUserWithCode:
    @staticmethod
    def _create_code(user, activation_code_generator, activation_code_storage):
        code = activation_code_generator.create_code()
        activation_code_storage.save_activation_code(username=user.username, code=code)
        return code

    def test_activate_user_with_code(
        self,
        mediator,
        uow,
        deactivated_user,
        activation_code_generator,
        activation_code_storage,
    ):
        uow.user_repository.add(deactivated_user)
        code = self._create_code(
            deactivated_user, activation_code_generator, activation_code_storage
        )

        mediator.handle(
            ActivateUserWithCode(username=deactivated_user.username, code=code)
        )

        assert deactivated_user.is_active

    def test_wrong_code(self, mediator, uow, deactivated_user):
        uow.user_repository.add(deactivated_user)
        code = "wrong-token"

        with pytest.raises(CodeVerificationError):
            mediator.handle(
                ActivateUserWithCode(username=deactivated_user.username, code=code)
            )

    def test_already_active_user(
        self,
        mediator,
        uow,
        activated_user,
        valid_password,
        activation_code_generator,
        activation_code_storage,
    ):
        uow.user_repository.add(activated_user)
        code = self._create_code(
            activated_user, activation_code_generator, activation_code_storage
        )

        with pytest.raises(UserAlreadyActive):
            mediator.handle(
                ActivateUserWithCode(username=activated_user.username, code=code)
            )


class TestResendActivationCode:
    def test_resend_activation_code(
        self, caplog, mediator, uow, deactivated_user, valid_password
    ):
        caplog.set_level(logging.INFO)
        uow.user_repository.add(deactivated_user)

        command = ResendActivationCode(
            username=deactivated_user.username, password=valid_password
        )
        mediator.handle(command)

        assert deactivated_user.email in caplog.text

    def test_resend_activation_code_non_existing_user(
        self, mediator, uow, valid_password
    ):
        command = ResendActivationCode(
            username="non-existing-user", password=valid_password
        )
        with pytest.raises(UserNotFound):
            mediator.handle(command)

    def test_resend_activation_code_wrong_password(
        self, mediator, uow, deactivated_user
    ):
        uow.user_repository.add(deactivated_user)

        command = ResendActivationCode(
            username=deactivated_user.username, password="wrong-password"
        )
        with pytest.raises(PasswordVerificationError):
            mediator.handle(command)

    def test_resend_activation_code_already_active(
        self, mediator, uow, activated_user, valid_password
    ):
        uow.user_repository.add(activated_user)

        command = ResendActivationCode(
            username=activated_user.username, password=valid_password
        )
        with pytest.raises(UserActive):
            mediator.handle(command)


class TestDeactivateUser:
    def test_deactivate_user(self, mediator, uow, activated_user):
        uow.user_repository.add(activated_user)
        mediator.handle(DeactivateUser(username=activated_user.username))
        assert activated_user.is_active is False

    def test_deactivate_non_existing_user(self, mediator):
        with pytest.raises(UserNotFound):
            mediator.handle(DeactivateUser(username="non-existing-user"))

    def test_deactivate_non_active_user(self, mediator, uow, deactivated_user):
        uow.user_repository.add(deactivated_user)
        with pytest.raises(UserAlreadyDeactivated):
            mediator.handle(DeactivateUser(username=deactivated_user.username))
