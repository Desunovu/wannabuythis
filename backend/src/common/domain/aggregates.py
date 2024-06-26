from src.common.domain.events import DomainEvent


class AggregateRoot:
    def __init__(self):
        self.events = []

    def add_event(self, event: DomainEvent):
        self.events.append(event)
