from src.shared_kernel.events import DomainEvent


class AggregateRoot:
    def __init__(self, id: int):
        self.id = id
        self.events = []

    def add_event(self, event: DomainEvent):
        self.events.append(event)
