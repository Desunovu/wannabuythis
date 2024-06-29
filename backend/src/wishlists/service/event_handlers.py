from src.common.domain.events import DomainEvent
from src.wishlists.domain.events import (
    WishlistCreated,
    WishlistNameChanged,
    WishlistItemAdded,
    WishlistItemRemoved,
    WishlistItemMarkedAsPurchased,
    WishlistItemMarkedAsNotPurchased,
    WishlistArchived,
    WishlistUnarchived,
)

WISHLIST_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    WishlistCreated: [],
    WishlistNameChanged: [],
    WishlistItemAdded: [],
    WishlistItemRemoved: [],
    WishlistItemMarkedAsPurchased: [],
    WishlistItemMarkedAsNotPurchased: [],
    WishlistArchived: [],
    WishlistUnarchived: [],
}
