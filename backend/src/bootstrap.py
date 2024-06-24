import inspect
from typing import Callable, Dict

from src.common.adapters.dependencies import (
    PasswordHasher,
    DefaultPasswordHasher,
    UUIDGenerator,
    DefaultUUIDGenerator,
    TokenManager,
    JWTManager,
    Notificator,
    EmailNotificator,
)
from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.messagebus import Messagebus
from src.common.service.uow import UnitOfWork
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.roles.service.role_handlers import ROLE_COMMAND_HANDLERS, ROLE_EVENT_HANDLERS
from src.users.service.event_handlers import USER_EVENT_HANDLERS
from src.users.service.user_auth_service import UserAuthService
from src.users.service.user_handlers import (
    USER_COMMAND_HANDLERS,
)
from src.wishlists.service.wishlist_handlers import (
    WISHLIST_COMMAND_HANDLERS,
    WISHLIST_EVENT_HANDLERS,
)


def bootstrap(
    uow: UnitOfWork = SQLAlchemyUnitOfWork,
    password_manager: PasswordHasher = DefaultPasswordHasher,
    uuid_generator: UUIDGenerator = DefaultUUIDGenerator,
        auth_token_manager: TokenManager = JWTManager,
        notificator: Notificator = EmailNotificator,
) -> Messagebus:
    """
    Initializes the application's core components and returns a configured Messagebus instance.
    Sets up handlers, declares essential dependencies, and injects these dependencies into the handlers.
    """
    # Setup service class that will be injected into handlers
    user_auth_service = UserAuthService(
        uow=uow, password_manager=password_manager, token_manager=auth_token_manager
    )

    # Combine handlers
    command_handlers = {
        **USER_COMMAND_HANDLERS,
        **WISHLIST_COMMAND_HANDLERS,
        **ROLE_COMMAND_HANDLERS,
    }
    event_handlers = {
        **USER_EVENT_HANDLERS,
        **WISHLIST_EVENT_HANDLERS,
        **ROLE_EVENT_HANDLERS,
    }
    # Declare dependencies
    dependencies = {
        "uow": uow,
        "user_auth_service": user_auth_service,
        "password_manager": password_manager,
        "uuid_generator": uuid_generator,
        "auth_token_manager": auth_token_manager,
        "notificator": notificator,
    }
    # Inject dependencies
    injected_command_handlers, injected_event_handlers = inject_dependencies(
        command_handlers, event_handlers, dependencies
    )

    return Messagebus(
        uow=uow,
        command_handlers=injected_command_handlers,
        event_handlers=injected_event_handlers,
        dependencies=dependencies,
    )


def build_handler_with_injected_dependencies(
    handler: Callable, dependencies: Dict
) -> Callable:
    """
    Builds a new handler function with injected dependencies based on the original handler's required parameters.

    Args:
        handler (Callable): The original handler function.
        dependencies (Dict): A dictionary mapping dependency names to their respective instances.

    Returns:
        Callable: A new handler function with injected dependencies.
    """
    params = inspect.signature(handler).parameters
    dependencies_to_inject = {
        name: dependencies[name] for name in params if name in dependencies
    }

    def injected_handler(message):
        return handler(message, **dependencies_to_inject)

    return injected_handler


def inject_dependencies(
    command_handlers: dict[type[Command], Callable],
    event_handlers: dict[type[DomainEvent], list[Callable]],
    dependencies,
):
    """
    Inject dependencies into command and event handlers.

    Args:
        command_handlers: A dictionary mapping command types to their handler functions.
        event_handlers: A dictionary mapping event types to lists of handler functions.
        dependencies: A dictionary mapping dependency names to their respective instances.

    Returns:
        Tuple: A tuple containing the injected command handlers and injected event handlers.
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
