from src.wishlists.domain.events import (
    WishlistItemAdded,
    WishlistItemRemoved,
)


def test_wishlist_can_add_item(wishlist, banana_item):
    """Test that a wishlist can add an item and that the ItemAdded event is published"""
    wishlist.add_item(banana_item)

    assert banana_item in wishlist.items
    assert wishlist.events[-1] == WishlistItemAdded(
        item_uuid=banana_item.uuid,
        wishlist_uuid=wishlist.uuid,
        name=banana_item.name,
        quantity=banana_item.quantity,
        measurement_unit=banana_item.measurement_unit.name,
        priority=banana_item.priority.value,
    )


def test_wishlist_can_remove_item(populated_wishlist):
    """Test that a wishlist can remove an item and that the WishlistItemRemoved event is published"""
    item = populated_wishlist.items[0]
    populated_wishlist.remove_item(item.uuid)

    assert item not in populated_wishlist.items
    assert populated_wishlist.events[-1] == WishlistItemRemoved(
        item_uuid=item.uuid, wishlist_uuid=populated_wishlist.uuid
    )
