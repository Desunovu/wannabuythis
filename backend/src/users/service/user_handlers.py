from src.common.adapters.dependencies import PasswordHasher
from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.exceptions import (
    UserNotFound,
    UserExists,
    PasswordValidationError,
    PasswordVerificationError,
    UserNotActive,
    UserAlreadyActive,
    RoleNotFound,
    UserDoesNotHaveRole,
    UserAlreadyHasRole,
)
from src.common.service.uow import UnitOfWork
from src.users.domain.commands import (
    CreateUser,
    ChangePassword,
    DeactivateUser,
    ActivateUser,
    ChangeUserEmail,
    AddRoleToUser,
    RemoveRoleFromUser,
)
from src.users.domain.events import (
    UserCreated,
    PasswordChanged,
    UserDeactivated,
    EmailChanged,
    RoleAddedToUser,
    RoleRemovedFromUser,
    UserActivated,
)
from src.users.domain.model import User


def handle_create_user(
    command: CreateUser,
    uow: UnitOfWork,
    password_manager: PasswordHasher,
):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if user:
            raise UserExists(command.username)
        if not User.validate_password(command.password):
            raise PasswordValidationError()
        password_hash = password_manager.hash_password(command.password)
        user = User(command.username, command.email, password_hash)
        uow.user_repository.add(user)
        user.add_event(UserCreated(user.username))
        uow.commit()


def handle_change_password(
    command: ChangePassword,
    uow: UnitOfWork,
    password_manager: PasswordHasher,
):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(command.username)
        if not User.validate_password(command.new_password):
            raise PasswordValidationError()
        if not command.called_by_admin:
            if not password_manager.verify_password(
                password=command.old_password, password_hash=user.password_hash
            ):
                raise PasswordVerificationError()
        new_password_hash = password_manager.hash_password(command.new_password)
        user.change_password_hash(new_password_hash)
        user.add_event(PasswordChanged(user.username))
        uow.commit()


def handle_change_user_email(command: ChangeUserEmail, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(command.username)
        user.change_email(command.new_email)
        uow.commit()


def handle_activate_user(command: ActivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(command.username)
        if user.is_active:
            raise UserAlreadyActive(command.username)
        user.activate()
        uow.commit()


def handle_deactivate_user(command: DeactivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(command.username)
        if not user.is_active:
            raise UserNotActive(command.username)
        user.deactivate()
        uow.commit()


def handle_add_role_to_user(command: AddRoleToUser, uow: UnitOfWork):
    with uow:
        role = uow.role_repository.get(name=command.role_name)
        if not role:
            raise RoleNotFound(command.role_name)
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(command.username)
        if user.has_role(role):
            raise UserAlreadyHasRole(command.username, command.role_name)
        user.add_role(role)
        uow.commit()


def handle_remove_role_from_user(command: RemoveRoleFromUser, uow: UnitOfWork):
    with uow:
        role = uow.role_repository.get(name=command.role_name)
        if not role:
            raise RoleNotFound(command.role_name)
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(command.username)
        if not user.has_role(role):
            raise UserDoesNotHaveRole(command.username, command.role_name)
        user.remove_role(role)
        uow.commit()


USER_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateUser: handle_create_user,
    ChangePassword: handle_change_password,
    ChangeUserEmail: handle_change_user_email,
    ActivateUser: handle_activate_user,
    DeactivateUser: handle_deactivate_user,
    AddRoleToUser: handle_add_role_to_user,
    RemoveRoleFromUser: handle_remove_role_from_user,
}

USER_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [],
    PasswordChanged: [],
    EmailChanged: [],
    UserActivated: [],
    UserDeactivated: [],
    RoleAddedToUser: [],
    RoleRemovedFromUser: [],
}
