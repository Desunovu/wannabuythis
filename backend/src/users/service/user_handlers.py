from src.common.adapters.dependencies import PasswordHasher
from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.exceptions import (
    UserNotFound,
    UserExists,
    PasswordValidationFailed,
    PasswordVerificationFailed,
    UserNotActive,
    UserAlreadyActive,
)
from src.common.service.uow import UnitOfWork
from src.users.domain.commands import (
    CreateUser,
    ChangePassword,
    DeactivateUser,
    ActivateUser,
    ChangeUserEmail,
)
from src.users.domain.events import (
    UserCreated,
    PasswordChanged,
    UserDeactivated,
    EmailChanged,
)
from src.users.domain.user import User


def handle_create_user(
    command: CreateUser,
    uow: UnitOfWork,
    password_manager: PasswordHasher,
):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if user:
            raise UserExists(f"User {command.username} already exists")
        if not User.validate_password(command.password):
            raise PasswordValidationFailed("Password is not valid")
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
            raise UserNotFound(f"User {command.username} not found")
        if not User.validate_password(command.new_password):
            raise PasswordValidationFailed("New password is not valid")
        if not command.called_by_admin:
            if not password_manager.verify_password(
                command.old_password, user.password_hash
            ):
                raise PasswordVerificationFailed("Old password is not correct")
        new_password_hash = password_manager.hash_password(command.new_password)
        user.change_password_hash(new_password_hash)
        user.add_event(PasswordChanged(user.username))
        uow.commit()


def handle_change_user_email(command: ChangeUserEmail, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(f"User {command.username} not found")
        user.change_email(command.new_email)
        uow.commit()


def handle_activate_user(command: ActivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(f"User {command.username} not found")
        if user.is_active:
            raise UserAlreadyActive(f"User {command.username} is already active")
        user.activate()
        uow.commit()


def handle_deactivate_user(command: DeactivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(f"User {command.username} not found")
        if not user.is_active:
            raise UserNotActive(f"User {command.username} is already deactivated")
        user.deactivate()
        uow.commit()


USER_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateUser: handle_create_user,
    ChangePassword: handle_change_password,
    ChangeUserEmail: handle_change_user_email,
    ActivateUser: handle_activate_user,
    DeactivateUser: handle_deactivate_user,
}

USER_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [],
    PasswordChanged: [],
    EmailChanged: [],
    UserDeactivated: [],
}
