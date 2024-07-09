from dataclasses import dataclass, field

from src.common.domain.events import DomainEvent


@dataclass(kw_only=True)
class AggregateRoot:
    events: list[DomainEvent] = field(default_factory=list, compare=False)

    def _add_event(self, event: DomainEvent):
        self.events.append(event)
