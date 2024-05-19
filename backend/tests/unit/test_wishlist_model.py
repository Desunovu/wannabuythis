from src.domain.wishlist.events import (
    WishlistItemAdded,
    WishlistItemRemoved,
)


def test_wishlist_can_add_item(wishlist, banana_item):
    """Test that a wishlist can add an item and that the ItemAdded event is published"""
    wishlist.add_item(banana_item)

    assert banana_item in wishlist.items
    assert wishlist.events[-1] == WishlistItemAdded(banana_item.uuid, banana_item.name)


def test_wishlist_can_remove_item(populated_wishlist):
    """Test that a wishlist can remove an item and that the WishlistItemRemoved event is published"""
    item = populated_wishlist.items[0]
    populated_wishlist.remove_item(item.uuid)

    assert item not in populated_wishlist.items
    assert populated_wishlist.events[-1] == WishlistItemRemoved(item.uuid)
