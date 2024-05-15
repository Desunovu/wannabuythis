def test_shopping_list_can_add_item(banana_item, shopping_list):
    shopping_list.add_item(banana_item)

    assert len(shopping_list.items) == 1
    assert shopping_list.items[0] == banana_item


def test_shopping_list_can_remove_item(
    banana_item, apple_item, populated_shopping_list
):
    # Delete banana item by id, apple should be left
    populated_shopping_list.remove_item(banana_item.id)

    assert len(populated_shopping_list.items) == 1
    assert populated_shopping_list.items[0] == apple_item
