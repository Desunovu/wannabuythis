"""
Bootstrap layer:
- Combine handlers
- Declare dependencies
- Initialize staff for application
- Give application a messagebus
"""

from src.common.service.messagebus import Messagebus
from src.common.service.unit_of_work import AbstractUnitOfWork
from src.users.service.user_handlers import (
    USER_COMMAND_HANDLERS,
    USER_EVENT_HANDLERS,
)
from src.wishlists.service.wishlist_handlers import (
    WISHLIST_COMMAND_HANDLERS,
    WISHLIST_EVENT_HANDLERS,
)


def bootstrap(
    uow: AbstractUnitOfWork,
) -> Messagebus:
    command_handlers = USER_COMMAND_HANDLERS | WISHLIST_COMMAND_HANDLERS
    event_handlers = USER_EVENT_HANDLERS | WISHLIST_EVENT_HANDLERS
    return Messagebus(
        uow=uow,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
    )
