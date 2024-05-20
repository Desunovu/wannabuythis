import hashlib

from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.exceptions import (
    UserNotFound,
    UserExists,
    InvalidPassword,
    InvalidOldPassword,
)
from src.common.service.unit_of_work import AbstractUnitOfWork
from src.users.domain.commands import CreateUser, ChangePassword
from src.users.domain.events import UserCreated, PasswordChanged
from src.users.domain.user import User


# TODO move hashlib dependency to Bootstrap layer (code should depend on get_password_hash callable)


def handle_create_user(command: CreateUser, uow: AbstractUnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if user:
            raise UserExists(f"User {command.username} already exists")
        # TODO dry up password validation
        if not User.validate_password(command.password):
            raise InvalidPassword("Password is not valid")
        # TODO dry up password hashing
        password_hash = hashlib.sha256(command.password.encode()).hexdigest()
        user = User(command.username, command.email, password_hash)
        uow.user_repository.add(user)
        user.add_event(UserCreated(user.username))
        uow.commit()


def handle_change_password(command: ChangePassword, uow: AbstractUnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(f"User {command.username} not found")
        # TODO dry up password validation
        if not User.validate_password(command.new_password):
            raise InvalidPassword("Password is not valid")
        if not command.called_by_admin:
            # TODO dry up password hashing
            old_password_hash = hashlib.sha256(
                command.old_password.encode()
            ).hexdigest()
            if user.password_hash != old_password_hash:
                raise InvalidOldPassword("Old password is not correct")
        # TODO dry up password hashing
        new_password_hash = hashlib.sha256(command.new_password.encode()).hexdigest()
        user.change_password_hash(new_password_hash)
        user.add_event(PasswordChanged(user.username))
        uow.commit()


USER_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateUser: handle_create_user,
    ChangePassword: handle_change_password,
}

USER_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [],
    PasswordChanged: [],
}
