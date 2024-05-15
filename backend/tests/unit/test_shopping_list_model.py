from src.shopping_list.domain.model import ShoppingList


def test_shopping_list_can_add_item(random_shopping_item):
    item = random_shopping_item(item_id=1)
    shopping_list = ShoppingList(name="Shopping list", items=[])
    shopping_list.add_item(item)

    assert len(shopping_list.items) == 1
    assert shopping_list.items[0] == item


def test_shopping_list_can_remove_item(random_shopping_item):
    first_item = random_shopping_item(item_id=1)
    second_item = random_shopping_item(item_id=2)
    shopping_list = ShoppingList(name="Shopping list", items=[first_item, second_item])
    shopping_list.remove_item(first_item.id)

    assert len(shopping_list.items) == 1
    assert shopping_list.items[0].id == second_item.id
