from dataclasses import dataclass

from src.shared_kernel.domain.events import Event


@dataclass
class ItemRemovalFailed(Event):
    id: int

    def __str__(self):
        return f"Failed to remove item with ID {self.id}"
