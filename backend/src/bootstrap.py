import inspect
from typing import Any, Callable

from src.common.adapters.activation_code_storage import ActivationCodeStorage
from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.logger import setup_logging
from src.common.service.messagebus import Messagebus
from src.common.service.uow import UnitOfWork
from src.common.utils.activation_code_generator import ActivationCodeGenerator
from src.common.utils.notificator import Notificator
from src.common.utils.password_manager import PasswordManager
from src.common.utils.token_manager import TokenManager
from src.common.utils.uuid_generator import UUIDGenerator
from src.users.service.command_handlers import USER_COMMAND_HANDLERS
from src.users.service.event_handlers import USER_EVENT_HANDLERS
from src.wishlists.service.command_handlers import WISHLIST_COMMAND_HANDLERS
from src.wishlists.service.event_handlers import WISHLIST_EVENT_HANDLERS

COMMAND_HANDLERS = {
    **USER_COMMAND_HANDLERS,
    **WISHLIST_COMMAND_HANDLERS,
}
EVENT_HANDLERS = {
    **USER_EVENT_HANDLERS,
    **WISHLIST_EVENT_HANDLERS,
}


def build_handler_with_injected_dependencies(
    handler: Callable, dependencies: dict
) -> Callable:
    """
    Builds a new handler function with injected dependencies based on the original handler's required parameters.
    """
    params = inspect.signature(handler).parameters
    dependencies_to_inject = {
        name: dependencies[name] for name in params if name in dependencies
    }

    def injected_handler(message):
        return handler(message, **dependencies_to_inject)

    injected_handler.__name__ = handler.__name__

    return injected_handler


def inject_dependencies(
    command_handlers: dict[type[Command], Callable],
    event_handlers: dict[type[DomainEvent], list[Callable]],
    dependencies,
):
    """
    Inject dependencies into command and event handlers. Returns a tuple containing the injected command handlers and injected event handlers.
    """
    injected_command_handlers = {
        command_type: build_handler_with_injected_dependencies(handler, dependencies)
        for command_type, handler in command_handlers.items()
    }
    injected_event_handlers = {
        event_type: [
            build_handler_with_injected_dependencies(handler, dependencies)
            for handler in handlers
        ]
        for event_type, handlers in event_handlers.items()
    }
    return injected_command_handlers, injected_event_handlers


def initialize_messagebus(dependencies: dict[str, Any]) -> Messagebus:
    """Prepares handlers with injected dependencies and returns a configured Messagebus instance."""

    setup_logging("messagebus")

    injected_command_handlers, injected_event_handlers = inject_dependencies(
        command_handlers=COMMAND_HANDLERS,
        event_handlers=EVENT_HANDLERS,
        dependencies=dependencies,
    )

    return Messagebus(
        uow=dependencies["uow"],
        command_handlers=injected_command_handlers,
        event_handlers=injected_event_handlers,
        dependencies=dependencies,
    )


def create_dependencies_dict(
    uow: UnitOfWork,
    password_manager: PasswordManager,
    uuid_generator: UUIDGenerator,
    activation_code_generator: ActivationCodeGenerator,
    activation_code_storage: ActivationCodeStorage,
    token_manager: TokenManager,
    notificator: Notificator,
) -> dict[str, Any]:
    """Declares dependencies"""

    return {
        "uow": uow,
        "password_manager": password_manager,
        "uuid_generator": uuid_generator,
        "activation_code_generator": activation_code_generator,
        "activation_code_storage": activation_code_storage,
        "token_manager": token_manager,
        "notificator": notificator,
    }
