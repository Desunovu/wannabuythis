from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.uow import UnitOfWork

# At this point dependencies should be injected in handlers by bootstrap script (see src/bootstrap.py)
# So we don't need to pass any dependencies to handlers. Usage: handler_name(message)


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

    def handle(self, message: Command | DomainEvent):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Command):
                self._handle_command(message)
            elif isinstance(message, DomainEvent):
                self._handle_event(message)
            else:
                raise Exception(f"Unknown message type in messagebus: {type(message)}")

    def _handle_command(self, command: Command):
        try:
            command_handler = self.command_handlers[type(command)]
            command_handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            raise

    def _handle_event(self, event: DomainEvent):
        for event_handler in self.event_handlers[type(event)]:
            try:
                event_handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                continue
