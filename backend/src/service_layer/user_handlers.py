import hashlib

from src.domain.shared_kernel.commands import Command
from src.domain.shared_kernel.events import DomainEvent
from src.domain.user.commands import CreateUser, ChangePassword
from src.domain.user.events import UserCreated, PasswordChanged
from src.domain.user.user import User
from src.service_layer.unit_of_work import AbstractUnitOfWork


class UserNotFound(Exception):
    pass


class UserExists(Exception):
    pass


def handle_create_user(command: CreateUser, uow: AbstractUnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if user:
            raise UserExists(f"User {command.username} already exists")
        user = User(command.username, command.email, command.password_hash)
        uow.user_repository.add(user)
        user.add_event(UserCreated(user.username))
        uow.commit()


def handle_change_password(command: ChangePassword, uow: AbstractUnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.username)
        if not user:
            raise UserNotFound(f"User {command.username} not found")
        # TODO check user can change password (domain rule)

        # TODO move hashlib dependency to Bootstrap layer (depend on get_password_hash callable)
        # TODO Or even move to domain???
        password_hash = hashlib.sha256(command.password.encode()).hexdigest()
        user.change_password_hash(password_hash)
        user.add_event(PasswordChanged(user.username))
        uow.commit()


COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateUser: handle_create_user,
    ChangePassword: handle_change_password,
}

EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [lambda event: print(f"User {event.username} created")],
    PasswordChanged: [lambda event: print(f"User {event.username} password changed")],
}
