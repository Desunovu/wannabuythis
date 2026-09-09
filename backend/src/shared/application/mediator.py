import logging
from typing import Any, Callable

from dishka import Container
from dishka.integrations.base import wrap_injection

from src.shared.application.exceptions import ApplicationException
from src.shared.application.uow import UnitOfWork
from src.shared.domain.commands import Command
from src.shared.domain.events import DomainEvent

logger = logging.getLogger(__name__)


class Mediator:
    """Dispatches commands and domain events within the current REQUEST scope.

    Handler dependencies are declared with ``FromDishka[...]`` and injected by
    the container via ``wrap_injection`` — no manual signature introspection.
    """

    def __init__(
        self,
        container: Container,
        command_handlers: dict[type[Command], Callable] | None = None,
        event_handlers: dict[type[DomainEvent], list[Callable]] | None = None,
    ):
        self._container = container
        self._command_handlers: dict[type[Command], Callable] = {}
        self._event_handlers: dict[type[DomainEvent], list[Callable]] = {}
        if command_handlers:
            for command_type, handler in command_handlers.items():
                self.register_command(command_type, handler)
        if event_handlers:
            for event_type, handlers in event_handlers.items():
                for handler in handlers:
                    self.register_event(event_type, handler)

    def _inject(self, handler: Callable) -> Callable:
        return wrap_injection(
            func=handler,
            container_getter=lambda *args, **kwargs: self._container,
        )

    def register_command(self, command_type: type[Command], handler: Callable) -> None:
        self._command_handlers[command_type] = self._inject(handler)

    def register_event(self, event_type: type[DomainEvent], handler: Callable) -> None:
        self._event_handlers.setdefault(event_type, []).append(self._inject(handler))

    def _handle_command(
        self,
        command: Command,
        queue: list[Command | DomainEvent],
    ) -> Any:
        try:
            handler = self._command_handlers[type(command)]
            result = handler(command)
            queue.extend(self._container.get(UnitOfWork).collect_new_events())
            logger.info("Command %s handled by %s", command, handler.__name__)
            return result
        except ApplicationException as e:
            logger.error("Failed to handle command %s: %s", command, e)
            raise
        except Exception as e:
            logger.exception("Unexpected error handling command %s: %s", command, e)
            raise

    def _handle_event(
        self,
        event: DomainEvent,
        queue: list[Command | DomainEvent],
    ) -> None:
        for handler in self._event_handlers.get(type(event), []):
            try:
                handler(event)
                queue.extend(self._container.get(UnitOfWork).collect_new_events())
                logger.info("Event %s handled by %s", event, handler.__name__)
            except ApplicationException as e:
                logger.warning(
                    "Failed to handle event %s by %s: %s",
                    event,
                    handler.__name__,
                    e,
                )
            except Exception as e:
                logger.exception(
                    "Unexpected error handling event %s by %s: %s",
                    event,
                    handler.__name__,
                    e,
                )

    def handle(self, message: Command | DomainEvent) -> Any:
        """Process the message and all domain events raised while handling it."""
        queue: list[Command | DomainEvent] = [message]
        result = None

        while queue:
            msg = queue.pop(0)
            if isinstance(msg, Command):
                result = self._handle_command(msg, queue)
            elif isinstance(msg, DomainEvent):
                self._handle_event(msg, queue)
            else:
                raise TypeError(f"Unknown message type: {type(msg)}")

        return result
