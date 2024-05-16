from dataclasses import dataclass

from src.shared_kernel.domain.events import Event


@dataclass
class ShoppingListRemovalFailed(Event):
    id: int

    def __str__(self):
        return f"Failed to remove shopping list with ID {self.id}"
