from src.shared_kernel.domain.entity import AggregateRoot
from src.shopping_list.domain.model import ShoppingList
from src.user.domain.events import ShoppingListRemovalFailed


class User(AggregateRoot):

    def __init__(
        self,
        username: str,
        email: str,
        password_hash: str,
        shopping_lists: list[ShoppingList],
    ):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.shopping_lists = shopping_lists

    def add_shopping_list(self, shopping_list: ShoppingList):
        self.shopping_lists.append(shopping_list)

    def remove_shopping_list(self, shopping_list_id: int):
        try:
            shopping_list = next(
                sl for sl in self.shopping_lists if sl.id == shopping_list_id
            )
            self.shopping_lists.remove(shopping_list)
        except StopIteration:
            self.events.append(ShoppingListRemovalFailed(id=shopping_list_id))
