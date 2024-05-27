from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.exceptions import (
    RoleAlreadyExists,
    RoleNotFound,
    RoleAlreadyHasPermission,
    RoleDoesNotHavePermission,
)
from src.common.service.uow import UnitOfWork
from src.roles.domain.commands import (
    AddPermissionToRole,
    RemovePermissionFromRole,
    CreateRole,
)
from src.roles.domain.events import (
    RoleCreated,
    PermissionAddedToRole,
    PermissionRemovedFromRole,
)
from src.roles.domain.model import Role, Permission


def handle_create_role(command: CreateRole, uow: UnitOfWork):
    with uow:
        role = uow.role_repository.get(command.name)
        if role:
            raise RoleAlreadyExists(command.name)
        uow.role_repository.add(Role(command.name))
        uow.commit()


def handle_add_permission_to_role(command: AddPermissionToRole, uow: UnitOfWork):
    with uow:
        role = uow.role_repository.get(command.role_name)
        if not role:
            raise RoleNotFound(command.role_name)
        if role.has_permission(command.permission_name):
            raise RoleAlreadyHasPermission(command.role_name, command.permission_name)
        role.add_permission(Permission(command.permission_name))
        uow.commit()


def handle_remove_permission_from_role(
    command: RemovePermissionFromRole, uow: UnitOfWork
):
    with uow:
        role = uow.role_repository.get(command.role_name)
        if not role:
            raise RoleNotFound(command.role_name)
        if not role.has_permission(command.permission_name):
            raise RoleDoesNotHavePermission(command.role_name, command.permission_name)
        role.remove_permission(command.permission_name)
        uow.commit()


ROLE_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateRole: handle_create_role,
    AddPermissionToRole: handle_add_permission_to_role,
    RemovePermissionFromRole: handle_remove_permission_from_role,
}

ROLE_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    RoleCreated: [],
    PermissionAddedToRole: [],
    PermissionRemovedFromRole: [],
}
