from src.modules.wishlists.domain.events import (
    WishlistArchived,
    WishlistCreated,
    WishlistItemAdded,
    WishlistItemMarkedAsNotPurchased,
    WishlistItemMarkedAsPurchased,
    WishlistItemRemoved,
    WishlistNameChanged,
    WishlistUnarchived,
)
from src.shared.domain.events import DomainEvent

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
