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
    def test_change_password_by_admin(self, messagebus, user, valid_password):
        messagebus.uow.user_repository.add(user)
        old_password_hash = user.password_hash
        messagebus.handle(
            ChangePassword("testuser", valid_password, called_by_admin=True)
        )

        assert user.password_hash != old_password_hash

    def test_change_password_by_user(
        self, messagebus, valid_password, valid_old_password
    ):
        # We should create a user by command to know user's old password and generate real password hash
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

    def test_change_password_wrong_old_password(self, messagebus, user, valid_password):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(PasswordVerificationFailed):
            messagebus.handle(
                ChangePassword("testuser", valid_password, "invalid-old-password")
            )

    def test_change_password_invalid_password(
        self, messagebus, invalid_password, valid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        with pytest.raises(PasswordValidationFailed):
            messagebus.handle(
                ChangePassword("testuser", invalid_password, valid_old_password)
            )


class TestChangeUserEmail:
    def test_update_user_email(self, messagebus, user):
        messagebus.uow.user_repository.add(user)
        messagebus.handle(ChangeUserEmail(username=user.username, new_email="newemail"))
        assert user.email == "newemail"

    def test_update_user_email_non_existing_user(self, messagebus):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                ChangeUserEmail(username="non-existing-user", new_email="newemail")
            )


class TestActivateUser:
    def test_activate_user(self, messagebus, user):
        user.is_active = False
        messagebus.uow.user_repository.add(user)
        assert user.is_active is False
        messagebus.handle(ActivateUser(username=user.username))
        assert user.is_active is True

    def test_activate_non_existing_user(self, messagebus):
        with pytest.raises(UserNotFound):
            messagebus.handle(ActivateUser(username="non-existing-user"))

    def test_activate_already_active_user(self, messagebus, user):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(UserAlreadyActive):
            messagebus.handle(ActivateUser(username=user.username))


class TestDeactivateUser:
    def test_deactivate_user(self, messagebus, user):
        messagebus.uow.user_repository.add(user)
        assert user.is_active is True
        messagebus.handle(DeactivateUser(username=user.username))
        assert user.is_active is False

    def test_deactivate_non_existing_user(self, messagebus):
        with pytest.raises(UserNotFound):
            messagebus.handle(DeactivateUser(username="non-existing-user"))

    def test_deactivate_non_active_user(self, messagebus, user):
        user.is_active = False
        messagebus.uow.user_repository.add(user)
        with pytest.raises(UserNotActive):
            messagebus.handle(DeactivateUser(username=user.username))


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

    def test_add_role_to_user_already_has_role(self, messagebus, user, admin_role):
        messagebus.uow.user_repository.add(user)
        messagebus.uow.role_repository.add(admin_role)
        messagebus.handle(
            AddRoleToUser(username=user.username, role_name=admin_role.name)
        )
        with pytest.raises(UserAlreadyHasRole):
            messagebus.handle(
                AddRoleToUser(username=user.username, role_name=admin_role.name)
            )

    def test_add_role_to_user_non_existing_role(self, messagebus, user):
        messagebus.uow.user_repository.add(user)
        with pytest.raises(RoleNotFound):
            messagebus.handle(
                AddRoleToUser(username=user.username, role_name="non-existing-role")
            )


class TestRemoveRoleFromUser:
    def test_remove_role_from_user(self, messagebus, user, admin_role):
        messagebus.uow.user_repository.add(user)
        messagebus.uow.role_repository.add(admin_role)
        messagebus.handle(
            AddRoleToUser(username=user.username, role_name=admin_role.name)
        )
        assert user.has_role(admin_role)
        messagebus.handle(
            RemoveRoleFromUser(username=user.username, role_name=admin_role.name)
        )
        assert not user.has_role(admin_role)

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
        messagebus.uow.role_repository.add(admin_role)
        messagebus.uow.user_repository.add(user)
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
