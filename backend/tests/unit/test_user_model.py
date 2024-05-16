from src.user.domain.events import ShoppingListRemovalFailed


def test_user_can_add_shopping_list(user, shopping_list):
    user.add_shopping_list(shopping_list)

    assert len(user.shopping_lists) == 1
    assert user.shopping_lists[0] == shopping_list


def test_user_can_remove_shopping_list(user_with_shopping_lists):
    shopping_list_to_remove = user_with_shopping_lists.shopping_lists[0]
    user_with_shopping_lists.remove_shopping_list(shopping_list_to_remove.id)

    assert shopping_list_to_remove not in user_with_shopping_lists.shopping_lists


def test_user_shopping_list_removal_failed_event_is_published(
    user_with_shopping_lists,
):
    shopping_list_to_remove = user_with_shopping_lists.shopping_lists[0]
    # Delete first shopping list 2 times
    for _ in range(2):
        user_with_shopping_lists.remove_shopping_list(shopping_list_to_remove.id)

    assert user_with_shopping_lists.events[-1] == ShoppingListRemovalFailed(
        id=shopping_list_to_remove.id
    )
