import logging
from typing import Any

from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.exceptions import ApplicationException
from src.common.service.uow import UnitOfWork

# Dependencies should be injected in handlers by bootstrap script (see src/bootstrap.py)
# So we don't need to pass any dependencies to handlers. Usage: handler_name(message)

logger = logging.getLogger("messagebus")


class Messagebus:
    def __init__(
        self,
        uow: UnitOfWork,
        command_handlers: dict[type[Command], callable],
        event_handlers: dict[type[DomainEvent], list[callable]],
        dependencies: dict[str, object],
    ):
        self.uow = uow
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers
        self.dependencies = dependencies
        self.queue = []

    def _handle_command(self, command: Command) -> Any:
        try:
            command_handler = self.command_handlers[type(command)]
            result = command_handler(command)
            self.queue.extend(self.uow.collect_new_events())
            logger.info(
                f"Command {command} handled successfully by {command_handler.__name__}"
            )
            return result
        except ApplicationException as e:
            logger.error(
                f"Failed to handle command {command}: {e}"
            )
            raise e
        except Exception as e:
            logger.exception(f"Failed to handle command {command}. Exception: {e}")
            raise e

    def _handle_event(self, event: DomainEvent):
        for event_handler in self.event_handlers[type(event)]:
            try:
                event_handler(event)
                self.queue.extend(self.uow.collect_new_events())
                logger.info(
                    f"Event {event} handled successfully by {event_handler.__name__}"
                )
            except ApplicationException as e:
                logger.warning(
                    f"Failed to handle event {event} by {event_handler.__name__}: {e}"
                )
            except Exception as e:
                logger.exception(
                    f"Failed to handle event {event} by {event_handler.__name__}. Exception: {e}"
                )
                continue

    def handle(self, message: Command | DomainEvent):
        """
        Handles all messages in the queue.
        This should be the only result, because there should be a single command in the messagebus queue
        """
        self.queue = [message]
        result = None
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Command):
                result = self._handle_command(message)
            elif isinstance(message, DomainEvent):
                self._handle_event(message)
            else:
                raise Exception(f"Unknown message type in messagebus: {type(message)}")
        return result
