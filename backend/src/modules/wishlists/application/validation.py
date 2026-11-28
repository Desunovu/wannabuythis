from uuid import UUID

from src.shared.application.exceptions import (
    WishlistItemQuantityInvalid,
    WishlistItemsLimitExceeded,
)


def validate_item_quantity(quantity: int, max_quantity: int) -> None:
    """Apply the configurable upper bound; positivity is a domain invariant."""
    if quantity > max_quantity:
        raise WishlistItemQuantityInvalid(
            f"Wishlist item quantity must not exceed {max_quantity}"
        )


def validate_items_count(wishlist_uuid: UUID, items_count: int, max_count: int) -> None:
    """Reject adding an item once the wishlist holds the configured maximum."""
    if items_count >= max_count:
        raise WishlistItemsLimitExceeded(wishlist_uuid, max_count)
