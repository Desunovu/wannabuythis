from src.shared_kernel.domain.entity import AggregateRoot
from src.shopping_list.domain.model import ShoppingList


class User(AggregateRoot):
    username: str
    email: str
    password_hash: str
    shopping_lists: list[ShoppingList]

    def add_shopping_list(self, shopping_list: ShoppingList):
        pass

    def remove_shopping_list(self, shopping_list_id: int):
        pass
