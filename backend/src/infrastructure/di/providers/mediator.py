from collections.abc import Iterable

from dishka import Container, Provider, Scope, provide
from dishka.integrations.base import wrap_injection

from src.modules.users.application.command_handlers import USER_COMMAND_HANDLERS
from src.modules.users.application.event_handlers import USER_EVENT_HANDLERS
from src.modules.wishlists.application.command_handlers import WISHLIST_COMMAND_HANDLERS
from src.modules.wishlists.application.event_handlers import WISHLIST_EVENT_HANDLERS
from src.shared.application.mediator import Mediator
from src.shared.application.uow import UnitOfWork
from src.shared.domain.events import DomainEvent


def _wrap_handler(handler, container: Container):
    return wrap_injection(
        func=handler,
        container_getter=lambda *args, **kwargs: container,
    )


def _make_collect_events(container: Container):
    def collect_events() -> Iterable[DomainEvent]:
        return container.get(UnitOfWork).collect_new_events()

    return collect_events


class MediatorProvider(Provider):
    @provide(scope=Scope.REQUEST)  # TODO: do not wrap handlers within request scope
    def get_mediator(self, container: Container) -> Mediator:
        raw_command_handlers = {**USER_COMMAND_HANDLERS, **WISHLIST_COMMAND_HANDLERS}
        raw_event_handlers = {**USER_EVENT_HANDLERS, **WISHLIST_EVENT_HANDLERS}

        command_handlers = {
            cmd: _wrap_handler(handler, container)
            for cmd, handler in raw_command_handlers.items()
        }
        event_handlers = {
            evt: [_wrap_handler(h, container) for h in handlers]
            for evt, handlers in raw_event_handlers.items()
        }

        return Mediator(
            collect_events=_make_collect_events(container),
            command_handlers=command_handlers,
            event_handlers=event_handlers,
        )
