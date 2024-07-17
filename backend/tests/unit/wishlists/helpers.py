from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.wishlists.domain.model import Wishlist


def find_purchased_item(wishlist: "Wishlist"):
    return next(item for item in wishlist.items if item.is_purchased)


def find_not_purchased_item(wishlist: "Wishlist"):
    return next(item for item in wishlist.items if not item.is_purchased)
