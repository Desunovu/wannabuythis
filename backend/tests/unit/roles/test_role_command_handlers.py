import pytest

from src.common.service.exceptions import (
    RoleAlreadyExists,
    RoleNotFound,
    RoleDoesNotHavePermission,
)
from src.roles.domain.commands import (
    CreateRole,
    AddPermissionToRole,
    RemovePermissionFromRole,
)
from src.roles.domain.model import Permission


class TestCreateRole:
    def test_create_role(self, messagebus):
        messagebus.handle(CreateRole("test_role"))
        assert messagebus.uow.role_repository.get("test_role") is not None

    def test_create_role_with_existing_name(self, messagebus, default_role):
        messagebus.uow.role_repository.add(default_role)
        with pytest.raises(RoleAlreadyExists):
            messagebus.handle(CreateRole(default_role.name))


class TestAddPermissionToRole:
    def test_add_permission_to_role(self, messagebus, default_role, permission):
        messagebus.uow.role_repository.add(default_role)
        messagebus.handle(
            AddPermissionToRole(
                role_name=default_role.name, permission_name=permission.name
            )
        )
        assert permission in default_role.permissions

    def test_add_permission_to_role_with_non_existing_role(
        self, messagebus, permission
    ):
        with pytest.raises(RoleNotFound):
            messagebus.handle(
                AddPermissionToRole(
                    role_name="non_existing_role", permission_name=permission.name
                )
            )

    def test_add_permission_to_role_with_non_existing_permission(
        self, messagebus, default_role
    ):
        messagebus.uow.role_repository.add(default_role)
        messagebus.handle(
            AddPermissionToRole(
                role_name=default_role.name, permission_name="non_existing_permission"
            )
        )
        assert Permission("non_existing_permission") in default_role.permissions


class TestRemovePermissionFromRole:
    def test_remove_permission_from_role(
        self, messagebus, role_with_permissions, permission
    ):
        messagebus.uow.role_repository.add(role_with_permissions)
        messagebus.handle(
            RemovePermissionFromRole(
                role_name=role_with_permissions.name, permission_name=permission.name
            )
        )
        assert permission not in role_with_permissions.permissions

    def test_remove_permission_from_role_with_non_existing_role(
        self, messagebus, permission
    ):
        with pytest.raises(RoleNotFound):
            messagebus.handle(
                RemovePermissionFromRole(
                    role_name="non_existing_role", permission_name=permission.name
                )
            )

    def test_remove_permission_from_role_with_non_existing_permission(
        self, messagebus, default_role
    ):
        messagebus.uow.role_repository.add(default_role)
        with pytest.raises(RoleDoesNotHavePermission):
            messagebus.handle(
                RemovePermissionFromRole(
                    role_name=default_role.name,
                    permission_name="non_existing_permission",
                )
            )
