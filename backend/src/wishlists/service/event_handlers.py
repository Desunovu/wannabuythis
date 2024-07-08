from src.common.domain.events import DomainEvent
from src.wishlists.domain.events import (
    WishlistArchived,
    WishlistCreated,
    WishlistItemAdded,
    WishlistItemMarkedAsNotPurchased,
    WishlistItemMarkedAsPurchased,
    WishlistItemRemoved,
    WishlistNameChanged,
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
