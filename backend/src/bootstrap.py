import inspect

from src.common.adapters.dependencies import (
    PasswordHasher,
    DefaultPasswordHasher,
    UUIDGenerator,
    DefaultUUIDGenerator,
)
from src.common.service.messagebus import Messagebus
from src.common.service.uow import UnitOfWork
from src.users.service.user_handlers import (
    USER_COMMAND_HANDLERS,
    USER_EVENT_HANDLERS,
)
from src.wishlists.service.wishlist_handlers import (
    WISHLIST_COMMAND_HANDLERS,
    WISHLIST_EVENT_HANDLERS,
)


def bootstrap(
    uow: UnitOfWork,
    password_manager: PasswordHasher = DefaultPasswordHasher,
    uuid_generator: UUIDGenerator = DefaultUUIDGenerator,
) -> Messagebus:
    """
    Bootstrap script:
    - Combine handlers
    - Declare dependencies and provide them to handlers
    - Initialize staff for application
    - Give application a messagebus
    """

    # Dependencies injection
    command_handlers = USER_COMMAND_HANDLERS | WISHLIST_COMMAND_HANDLERS
    event_handlers = USER_EVENT_HANDLERS | WISHLIST_EVENT_HANDLERS
    dependencies = {
        "uow": uow,
        "password_manager": password_manager,
        "uuid_generator": uuid_generator,
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in command_handlers.items()
    }
    injected_event_handlers = {
        event_type: [inject_dependencies(handler, dependencies) for handler in handlers]
        for event_type, handlers in event_handlers.items()
    }

    return Messagebus(
        uow=uow,
        command_handlers=injected_command_handlers,
        event_handlers=injected_event_handlers,
    )


def inject_dependencies(handler, dependencies):
    """Builds a handler function with injected dependencies"""
    params = inspect.signature(handler).parameters
    dependencies_to_inject = {
        name: dependencies[name] for name in params if name in dependencies
    }
    return lambda message: handler(message, **dependencies_to_inject)
