from src.wishlist.domain.events import ItemAdded, ItemRemoved, ItemNotFound


def test_wishlist_can_add_item(banana_item, wishlist):
    """Test that a wishlist can add an item and that the ItemAdded event is published"""
    wishlist.add_item(banana_item)

    assert banana_item in wishlist.items
    assert wishlist.events[-1] == ItemAdded(wishlist.id, banana_item.id)


def test_wishlist_can_remove_item(populated_wishlist):
    """Test that a wishlist can remove an item and that the ItemRemoved event is published"""
    item = populated_wishlist.items[0]
    populated_wishlist.remove_item(item.id)

    assert item not in populated_wishlist.items
    assert populated_wishlist.events[-1] == ItemRemoved(populated_wishlist.id, item.id)


def test_wishlist_cannot_remove_item(populated_wishlist):
    """
    Test that ItemNotFound event is published  and nothing else happens if a wishlist tries to remove a non-existing item
    """
    items_copy = populated_wishlist.items[:]
    populated_wishlist.remove_item(999)

    assert items_copy == populated_wishlist.items
    assert populated_wishlist.events[-1] == ItemNotFound(populated_wishlist.id, 999)
