import pytest

from src.common.service.exceptions import (
    UserExists,
    UserNotFound,
    PasswordVerificationFailed,
    PasswordValidationFailed,
    UserAlreadyActive,
    UserNotActive,
    UserAlreadyHasRole,
    RoleNotFound,
    UserDoesNotHaveRole,
)
from src.users.domain.commands import (
    CreateUser,
    ChangePassword,
    ChangeUserEmail,
    ActivateUser,
    DeactivateUser,
    AddRoleToUser,
    RemoveRoleFromUser,
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
        with pytest.raises(PasswordValidationFailed):
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


class TestChangePassword:
    def test_change_password_by_admin(self, messagebus, user, valid_new_password):
        messagebus.uow.user_repository.add(user)
        old_password_hash = user.password_hash
        messagebus.handle(
            ChangePassword(
                username=user.username,
                new_password=valid_new_password,
                called_by_admin=True,
            )
        )
        assert user.password_hash != old_password_hash

    def test_change_password_by_user(
        self, messagebus, user, valid_password, valid_new_password
    ):
        messagebus.uow.user_repository.add(user)
        old_password_hash = user.password_hash
        messagebus.handle(
            ChangePassword(
                username=user.username,
                new_password=valid_new_password,
                old_password=valid_password,
            )
        )
        assert user.password_hash != old_password_hash

    def test_change_password_non_existing_user(self, messagebus, valid_new_password):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                ChangePassword(
                    username="non-existing-user",
                    new_password=valid_new_password,
                    called_by_admin=True,
                )
            )

    def test_change_password_wrong_old_password(
        self, messagebus, user, invalid_password, valid_new_password
    ):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(PasswordVerificationFailed):
            messagebus.handle(
                ChangePassword(
                    username=user.username,
                    new_password=valid_new_password,
                    old_password=invalid_password,
                )
            )

    def test_change_password_invalid_password(self, messagebus, user, invalid_password):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(PasswordValidationFailed):
            messagebus.handle(
                ChangePassword(
                    username=user.username,
                    new_password=invalid_password,
                    called_by_admin=True,
                )
            )


class TestChangeUserEmail:
    def test_update_user_email(self, messagebus, user, new_email):
        messagebus.uow.user_repository.add(user)
        messagebus.handle(ChangeUserEmail(username=user.username, new_email=new_email))
        assert user.email == new_email

    def test_update_user_email_non_existing_user(self, messagebus, new_email):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                ChangeUserEmail(username="non-existing-user", new_email=new_email)
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
        with pytest.raises(UserNotActive):
            messagebus.handle(DeactivateUser(username=deactivated_user.username))


class TestAddRoleToUser:
    def test_add_role_to_user(self, messagebus, user, admin_role):
        messagebus.uow.user_repository.add(user)
        messagebus.uow.role_repository.add(admin_role)
        messagebus.handle(
            AddRoleToUser(username=user.username, role_name=admin_role.name)
        )
        assert user.has_role(admin_role)

    def test_add_role_to_non_existing_user(self, messagebus, admin_role):
        messagebus.uow.role_repository.add(admin_role)
        with pytest.raises(UserNotFound):
            messagebus.handle(
                AddRoleToUser(username="non-existing-user", role_name=admin_role.name)
            )

    def test_add_role_to_user_already_has_role(
        self, messagebus, admin_user, admin_role
    ):
        messagebus.uow.user_repository.add(admin_user)
        messagebus.uow.role_repository.add(admin_role)
        with pytest.raises(UserAlreadyHasRole):
            messagebus.handle(
                AddRoleToUser(username=admin_user.username, role_name=admin_role.name)
            )

    def test_add_role_to_user_non_existing_role(self, messagebus, user):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(RoleNotFound):
            messagebus.handle(
                AddRoleToUser(username=user.username, role_name="non-existing-role")
            )


class TestRemoveRoleFromUser:
    def test_remove_role_from_user(self, messagebus, admin_user, admin_role):
        messagebus.uow.user_repository.add(admin_user)
        messagebus.uow.role_repository.add(admin_role)
        messagebus.handle(
            RemoveRoleFromUser(username=admin_user.username, role_name=admin_role.name)
        )
        assert not admin_user.has_role(admin_role)

    def test_remove_role_from_non_existing_user(self, messagebus, admin_role):
        messagebus.uow.role_repository.add(admin_role)
        with pytest.raises(UserNotFound):
            messagebus.handle(
                RemoveRoleFromUser(
                    username="non-existing-user", role_name=admin_role.name
                )
            )

    def test_remove_role_from_user_does_not_have_role(
        self, messagebus, user, admin_role
    ):
        messagebus.uow.user_repository.add(user)
        messagebus.uow.role_repository.add(admin_role)
        with pytest.raises(UserDoesNotHaveRole):
            messagebus.handle(
                RemoveRoleFromUser(username=user.username, role_name=admin_role.name)
            )

    def test_remove_role_from_user_non_existing_role(self, messagebus, user):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(RoleNotFound):
            messagebus.handle(
                RemoveRoleFromUser(
                    username=user.username, role_name="non-existing-role"
                )
            )
