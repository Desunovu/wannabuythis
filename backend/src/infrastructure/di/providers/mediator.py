from dishka import Container, Provider, Scope, provide

from src.modules.users.application.command_handlers import USER_COMMAND_HANDLERS
from src.modules.users.application.event_handlers import USER_EVENT_HANDLERS
from src.modules.wishlists.application.command_handlers import WISHLIST_COMMAND_HANDLERS
from src.modules.wishlists.application.event_handlers import WISHLIST_EVENT_HANDLERS
from src.shared.application.mediator import Mediator


class MediatorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_mediator(self, container: Container) -> Mediator:
        COMMAND_HANDLERS = {**USER_COMMAND_HANDLERS, **WISHLIST_COMMAND_HANDLERS}
        EVENT_HANDLERS = {**USER_EVENT_HANDLERS, **WISHLIST_EVENT_HANDLERS}
        return Mediator(
            container=container,
            command_handlers=COMMAND_HANDLERS,
            event_handlers=EVENT_HANDLERS,
        )