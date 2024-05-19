from src.domain.shared_kernel.commands import Command
from src.domain.shared_kernel.events import DomainEvent
from src.service_layer.unit_of_work import AbstractUnitOfWork


class Messagebus:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        command_handlers: dict[type[Command], callable],
        event_handlers: dict[type[DomainEvent], list[callable]],
    ):
        self.uow = uow
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers
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
            command_handler(command, self.uow)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            raise

    def _handle_event(self, event: DomainEvent):
        for event_handler in self.event_handlers[type(event)]:
            try:
                event_handler(event, self.uow)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                continue
