import datetime
import logging

import pytest

from src.modules.users.application.refresh_token_service import RefreshTokenService
from src.modules.users.domain.commands import (
    ActivateUser,
    ActivateUserWithCode,
    ChangeEmail,
    ChangePasswordWithOldPassword,
    ChangePasswordWithoutOldPassword,
    CreateUser,
    DeactivateUser,
    GenerateAuthToken,
    RefreshAccessToken,
    ResendActivationCode,
    RevokeRefreshToken,
)
from src.modules.users.domain.tokens import RefreshToken
from src.shared.application.exceptions import (
    CodeVerificationError,
    PasswordValidationError,
    PasswordVerificationError,
    TokenException,
    UserActive,
    UserAlreadyActive,
    UserAlreadyDeactivated,
    UserEmailExists,
    UserExists,
    UserInvalidName,
    UserNotActive,
    UserNotFound,
)


def _store_refresh_token(uow, username, token, expires_in):
    now = datetime.datetime.now(datetime.UTC)
    uow.refresh_token_repository.add(
        RefreshToken(
            username=username,
            token_hash=RefreshTokenService.hash_token(token),
            created_at=now,
            expires_at=now + expires_in,
        )
    )


def _issue_token_pair(mediator, username, password):
    return mediator.handle(GenerateAuthToken(username=username, password=password))


def _assert_refresh_token_revoked(uow, raw_token):
    stored = uow.refresh_token_repository.get_by_hash(
        RefreshTokenService.hash_token(raw_token)
    )
    assert stored is not None
    assert stored.is_revoked()


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

    def test_create_user_canonicalizes_email(self, mediator, uow, valid_password):
        mediator.handle(
            CreateUser(
                username="testuser",
                email="  Foo.Bar@Example.COM  ",
                password=valid_password,
            )
        )
        assert uow.user_repository.get("testuser").email == "foo.bar@example.com"

    def test_create_user_with_existing_email_ignoring_case(
        self, mediator, uow, user, valid_password
    ):
        uow.user_repository.add(user)
        with pytest.raises(UserEmailExists):
            mediator.handle(
                CreateUser(
                    username="anotheruser",
                    email="  TESTEMAIL@Example.com  ",
                    password=valid_password,
                )
            )


class TestGenerateAuthToken:
    def test_generate_auth_token_and_get_username(
        self, mediator, uow, user, valid_password
    ):
        uow.user_repository.add(user)
        token_pair = mediator.handle(
            GenerateAuthToken(
                username=user.username,
                password=valid_password,
            )
        )
        assert token_pair.access_token
        assert token_pair.refresh_token
        stored_refresh_token = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token(token_pair.refresh_token)
        )
        assert stored_refresh_token is not None
        assert stored_refresh_token.username == user.username

    def test_inactive_user_not_allowed_to_generate_auth_token(
        self, mediator, uow, deactivated_user, valid_password
    ):
        uow.user_repository.add(deactivated_user)
        command = GenerateAuthToken(
            username=deactivated_user.username,
            password=valid_password,
        )

        with pytest.raises(UserNotActive):
            mediator.handle(command)

    def test_generate_auth_token_wrong_username(self, mediator):
        with pytest.raises(UserNotFound):
            mediator.handle(
                GenerateAuthToken(
                    username="non-existing-user",
                    password="password",
                )
            )

    def test_generate_auth_token_wrong_password(self, mediator, uow, user):
        uow.user_repository.add(user)
        with pytest.raises(PasswordVerificationError):
            mediator.handle(
                GenerateAuthToken(
                    username=user.username,
                    password="wrong-password",
                )
            )

    def test_login_does_not_log_password(
        self, caplog, mediator, uow, user, valid_password
    ):
        caplog.set_level(logging.INFO)
        uow.user_repository.add(user)

        mediator.handle(
            GenerateAuthToken(
                username=user.username,
                password=valid_password,
            )
        )

        assert valid_password not in caplog.text


class TestRefreshAccessToken:
    def test_refresh_access_token(self, mediator, uow, user, valid_password):
        uow.user_repository.add(user)
        old_token_pair = mediator.handle(
            GenerateAuthToken(username=user.username, password=valid_password)
        )

        new_token_pair = mediator.handle(
            RefreshAccessToken(refresh_token=old_token_pair.refresh_token)
        )

        assert new_token_pair.access_token
        assert new_token_pair.refresh_token != old_token_pair.refresh_token
        old_refresh_token = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token(old_token_pair.refresh_token)
        )
        assert old_refresh_token is not None
        assert old_refresh_token.is_revoked()
        new_refresh_token = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token(new_token_pair.refresh_token)
        )
        assert new_refresh_token is not None
        assert not new_refresh_token.is_revoked()

    def test_refresh_access_token_rotates_pair_once(
        self, mediator, uow, user, valid_password
    ):
        uow.user_repository.add(user)
        token_pair = mediator.handle(
            GenerateAuthToken(username=user.username, password=valid_password)
        )
        mediator.handle(RefreshAccessToken(refresh_token=token_pair.refresh_token))

        with pytest.raises(TokenException):
            mediator.handle(RefreshAccessToken(refresh_token=token_pair.refresh_token))

    def test_refresh_access_token_with_unknown_token(self, mediator):
        with pytest.raises(TokenException):
            mediator.handle(RefreshAccessToken(refresh_token="unknown-token"))

    def test_refresh_access_token_with_expired_token(self, mediator, uow, user):
        _store_refresh_token(
            uow=uow,
            username=user.username,
            token="expired-token",
            expires_in=-datetime.timedelta(days=1),
        )
        uow.user_repository.add(user)

        with pytest.raises(TokenException):
            mediator.handle(RefreshAccessToken(refresh_token="expired-token"))

    def test_refresh_access_token_of_inactive_user(
        self, mediator, uow, deactivated_user
    ):
        _store_refresh_token(
            uow=uow,
            username=deactivated_user.username,
            token="deactivated-user-token",
            expires_in=datetime.timedelta(days=1),
        )
        uow.user_repository.add(deactivated_user)

        with pytest.raises(TokenException):
            mediator.handle(RefreshAccessToken(refresh_token="deactivated-user-token"))

    def test_refresh_access_token_of_inactive_user_with_revoked_token(
        self, mediator, uow, deactivated_user
    ):
        _store_refresh_token(
            uow=uow,
            username=deactivated_user.username,
            token="revoked-token",
            expires_in=datetime.timedelta(days=1),
        )
        uow.user_repository.add(deactivated_user)
        uow.refresh_token_repository.revoke(
            RefreshTokenService.hash_token("revoked-token"),
            revoked_at=datetime.datetime.now(datetime.UTC),
        )

        with pytest.raises(TokenException):
            mediator.handle(RefreshAccessToken(refresh_token="revoked-token"))

    def test_refresh_access_token_of_deleted_user(self, mediator, uow):
        _store_refresh_token(
            uow=uow,
            username="deleted-user",
            token="deleted-user-token",
            expires_in=datetime.timedelta(days=1),
        )

        with pytest.raises(TokenException):
            mediator.handle(RefreshAccessToken(refresh_token="deleted-user-token"))


class TestRevokeRefreshToken:
    def test_revoke_refresh_token(self, mediator, uow, user, valid_password):
        uow.user_repository.add(user)
        token_pair = mediator.handle(
            GenerateAuthToken(username=user.username, password=valid_password)
        )

        mediator.handle(RevokeRefreshToken(refresh_token=token_pair.refresh_token))

        stored_token = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token(token_pair.refresh_token)
        )
        assert stored_token is not None
        assert stored_token.is_revoked()

    def test_revoke_refresh_token_is_idempotent(
        self, mediator, uow, user, valid_password
    ):
        uow.user_repository.add(user)
        token_pair = mediator.handle(
            GenerateAuthToken(username=user.username, password=valid_password)
        )
        token_hash = RefreshTokenService.hash_token(token_pair.refresh_token)
        mediator.handle(RevokeRefreshToken(refresh_token=token_pair.refresh_token))
        revoked_at = uow.refresh_token_repository.get_by_hash(token_hash).revoked_at

        mediator.handle(RevokeRefreshToken(refresh_token=token_pair.refresh_token))

        assert (
            uow.refresh_token_repository.get_by_hash(token_hash).revoked_at
            == revoked_at
        )

    def test_revoke_unknown_refresh_token(self, mediator):
        mediator.handle(RevokeRefreshToken(refresh_token="unknown-token"))

    def test_revoke_expired_refresh_token(self, mediator, uow, user):
        _store_refresh_token(
            uow=uow,
            username=user.username,
            token="expired-token",
            expires_in=-datetime.timedelta(days=1),
        )

        mediator.handle(RevokeRefreshToken(refresh_token="expired-token"))

        stored_token = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token("expired-token")
        )
        assert stored_token.is_revoked()

    def test_revoke_refresh_token_revokes_only_supplied_session(
        self, mediator, uow, user, valid_password
    ):
        uow.user_repository.add(user)
        first_token_pair = mediator.handle(
            GenerateAuthToken(username=user.username, password=valid_password)
        )
        second_token_pair = mediator.handle(
            GenerateAuthToken(username=user.username, password=valid_password)
        )

        mediator.handle(
            RevokeRefreshToken(refresh_token=first_token_pair.refresh_token)
        )

        second_token = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token(second_token_pair.refresh_token)
        )
        assert second_token is not None
        assert not second_token.is_revoked()


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

    def test_change_password_by_admin_revokes_all_refresh_tokens(
        self, mediator, uow, user, valid_password, valid_new_password
    ):
        uow.user_repository.add(user)
        first_token_pair = _issue_token_pair(mediator, user.username, valid_password)
        second_token_pair = _issue_token_pair(mediator, user.username, valid_password)

        mediator.handle(
            ChangePasswordWithoutOldPassword(
                username=user.username,
                new_password=valid_new_password,
            )
        )

        _assert_refresh_token_revoked(uow, first_token_pair.refresh_token)
        _assert_refresh_token_revoked(uow, second_token_pair.refresh_token)

    def test_change_password_by_user_revokes_all_refresh_tokens(
        self, mediator, uow, user, valid_password, valid_new_password
    ):
        uow.user_repository.add(user)
        first_token_pair = _issue_token_pair(mediator, user.username, valid_password)
        second_token_pair = _issue_token_pair(mediator, user.username, valid_password)

        mediator.handle(
            ChangePasswordWithOldPassword(
                username=user.username,
                new_password=valid_new_password,
                old_password=valid_password,
            )
        )

        _assert_refresh_token_revoked(uow, first_token_pair.refresh_token)
        _assert_refresh_token_revoked(uow, second_token_pair.refresh_token)

    def test_change_password_revokes_only_target_user_tokens(
        self,
        mediator,
        uow,
        user,
        second_user,
        valid_password,
        valid_new_password,
    ):
        uow.user_repository.add(user)
        uow.user_repository.add(second_user)
        target_token_pair = _issue_token_pair(mediator, user.username, valid_password)
        other_token_pair = _issue_token_pair(
            mediator, second_user.username, valid_password
        )

        mediator.handle(
            ChangePasswordWithOldPassword(
                username=user.username,
                new_password=valid_new_password,
                old_password=valid_password,
            )
        )

        _assert_refresh_token_revoked(uow, target_token_pair.refresh_token)
        other_token = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token(other_token_pair.refresh_token)
        )
        assert other_token is not None
        assert not other_token.is_revoked()

    def test_failed_password_change_does_not_revoke_tokens(
        self, mediator, uow, user, invalid_password, valid_password, valid_new_password
    ):
        uow.user_repository.add(user)
        token_pair = _issue_token_pair(mediator, user.username, valid_password)

        with pytest.raises(PasswordVerificationError):
            mediator.handle(
                ChangePasswordWithOldPassword(
                    username=user.username,
                    new_password=valid_new_password,
                    old_password=invalid_password,
                )
            )

        stored = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token(token_pair.refresh_token)
        )
        assert stored is not None
        assert not stored.is_revoked()

    def test_invalid_new_password_does_not_revoke_tokens(
        self, mediator, uow, user, invalid_password, valid_password
    ):
        uow.user_repository.add(user)
        token_pair = _issue_token_pair(mediator, user.username, valid_password)

        with pytest.raises(PasswordValidationError):
            mediator.handle(
                ChangePasswordWithoutOldPassword(
                    username=user.username,
                    new_password=invalid_password,
                )
            )

        stored = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token(token_pair.refresh_token)
        )
        assert stored is not None
        assert not stored.is_revoked()

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

    def test_update_email_canonicalizes(self, mediator, uow, user):
        uow.user_repository.add(user)
        mediator.handle(
            ChangeEmail(username=user.username, new_email=" NEW@Example.COM ")
        )
        assert user.email == "new@example.com"

    def test_update_email_to_existing_email_ignoring_case(
        self, mediator, uow, user, second_user
    ):
        uow.user_repository.add(user)
        uow.user_repository.add(second_user)
        with pytest.raises(UserEmailExists):
            mediator.handle(
                ChangeEmail(username=user.username, new_email="SECONDUSER@example.com")
            )

    def test_update_email_to_own_email_ignoring_case(self, mediator, uow, user, email):
        uow.user_repository.add(user)
        mediator.handle(ChangeEmail(username=user.username, new_email=email.upper()))
        assert user.email == email


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

    def test_deactivate_user_revokes_all_refresh_tokens(
        self, mediator, uow, activated_user, valid_password
    ):
        uow.user_repository.add(activated_user)
        first_token_pair = _issue_token_pair(
            mediator, activated_user.username, valid_password
        )
        second_token_pair = _issue_token_pair(
            mediator, activated_user.username, valid_password
        )

        mediator.handle(DeactivateUser(username=activated_user.username))

        _assert_refresh_token_revoked(uow, first_token_pair.refresh_token)
        _assert_refresh_token_revoked(uow, second_token_pair.refresh_token)

    def test_deactivate_non_active_user_does_not_revoke_tokens(
        self, mediator, uow, deactivated_user
    ):
        _store_refresh_token(
            uow=uow,
            username=deactivated_user.username,
            token="inactive-user-token",
            expires_in=datetime.timedelta(days=1),
        )
        uow.user_repository.add(deactivated_user)

        with pytest.raises(UserAlreadyDeactivated):
            mediator.handle(DeactivateUser(username=deactivated_user.username))

        stored = uow.refresh_token_repository.get_by_hash(
            RefreshTokenService.hash_token("inactive-user-token")
        )
        assert stored is not None
        assert not stored.is_revoked()

    def test_deactivate_non_existing_user(self, mediator):
        with pytest.raises(UserNotFound):
            mediator.handle(DeactivateUser(username="non-existing-user"))

    def test_deactivate_non_active_user(self, mediator, uow, deactivated_user):
        uow.user_repository.add(deactivated_user)
        with pytest.raises(UserAlreadyDeactivated):
            mediator.handle(DeactivateUser(username=deactivated_user.username))
