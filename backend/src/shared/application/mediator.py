import logging
from collections.abc import Iterable
from typing import Any, Callable

from src.shared.application.exceptions import ApplicationException
from src.shared.domain.commands import Command
from src.shared.domain.events import DomainEvent

logger = logging.getLogger(__name__)


class Mediator:
    """Dispatches commands and domain events within the current REQUEST scope.

    Handlers arrive *already wrapped* for dependency injection — the mediator
    calls them as plain callables without knowing about any DI framework.
    """

    def __init__(
        self,
        collect_events: Callable[[], Iterable[DomainEvent]],
        command_handlers: dict[type[Command], Callable] | None = None,
        event_handlers: dict[type[DomainEvent], list[Callable]] | None = None,
    ):
        self._collect_events = collect_events
        self._command_handlers: dict[type[Command], Callable] = {}
        self._event_handlers: dict[type[DomainEvent], list[Callable]] = {}
        if command_handlers:
            for command_type, handler in command_handlers.items():
                self.register_command(command_type, handler)
        if event_handlers:
            for event_type, handlers in event_handlers.items():
                for handler in handlers:
                    self.register_event(event_type, handler)

    def register_command(self, command_type: type[Command], handler: Callable) -> None:
        self._command_handlers[command_type] = handler

    def register_event(self, event_type: type[DomainEvent], handler: Callable) -> None:
        self._event_handlers.setdefault(event_type, []).append(handler)

    def _handle_command(
        self,
        command: Command,
        queue: list[Command | DomainEvent],
    ) -> Any:
        try:
            handler = self._command_handlers[type(command)]
            result = handler(command)
            queue.extend(self._collect_events())
            logger.info(f"Command {command} handled by {handler.__name__}")
            return result
        except ApplicationException as e:
            logger.error(f"Failed to handle command {command}: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error handling command {command}: {e}")
            raise

    def _handle_event(
        self,
        event: DomainEvent,
        queue: list[Command | DomainEvent],
    ) -> None:
        for handler in self._event_handlers.get(type(event), []):
            try:
                handler(event)
                queue.extend(self._collect_events())
                logger.info(f"Event {event} handled by {handler.__name__}")
            except ApplicationException as e:
                logger.warning(
                    f"Failed to handle event {event} by {handler.__name__}: {e}",
                )
            except Exception as e:
                logger.exception(
                    f"Unexpected error handling event {event} by {handler.__name__}: {e}",
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
