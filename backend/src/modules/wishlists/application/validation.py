from src.shared.application.exceptions import WishlistItemQuantityInvalid


def validate_item_quantity(quantity: int, max_quantity: int) -> None:
    """Apply the configurable upper bound; positivity is a domain invariant."""
    if quantity > max_quantity:
        raise WishlistItemQuantityInvalid(
            f"Wishlist item quantity must not exceed {max_quantity}"
        )
