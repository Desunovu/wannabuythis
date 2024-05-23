from src.common.adapters.dependencies import AbstractUUIDGenerator
from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.exceptions import (
    WishlistNotFound,
    UserNotFound,
    WishlistItemNotFound,
)
from src.common.service.uow import AbstractUnitOfWork
from src.wishlists.domain.commands import (
    CreateWishlist,
    ChangeWishlistName,
    AddWishlistItem,
    RemoveWishlistItem,
)
from src.wishlists.domain.events import (
    WishlistNameChanged,
    WishlistCreated,
    WishlistItemAdded,
    WishlistItemRemoved,
)
from src.wishlists.domain.wishlist import Wishlist
from src.wishlists.domain.wishlist_item import WishlistItem, MeasurementUnit, Priority


def handle_create_wishlist(
    command: CreateWishlist,
    uow: AbstractUnitOfWork,
    uuid_generator: AbstractUUIDGenerator,
):
    with uow:
        user = uow.user_repository.get(username=command.owner_username)
        if not user:
            raise UserNotFound(
                f"User {command.owner_username} not found to create wishlist"
            )
        wishlist = Wishlist(
            uuid=uuid_generator.generate(),
            owner_username=command.owner_username,
            name=command.name,
            items=[],
        )
        uow.wishlist_repository.add(wishlist)
        wishlist.add_event(WishlistCreated(wishlist.uuid, wishlist.name))
        uow.commit()


def handle_change_wishlist_name(command: ChangeWishlistName, uow: AbstractUnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.uuid)
        if not wishlist:
            raise WishlistNotFound(f"Wishlist {command.uuid} not found")
        wishlist.change_name(command.new_name)
        wishlist.add_event(WishlistNameChanged(wishlist.uuid, wishlist.name))
        uow.commit()


def handle_add_wishlist_item(
    command: AddWishlistItem,
    uow: AbstractUnitOfWork,
    uuid_generator: AbstractUUIDGenerator,
):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
        if not wishlist:
            raise WishlistNotFound(f"Wishlist {command.wishlist_uuid} not found")
        item = WishlistItem(
            uuid=uuid_generator.generate(),
            wishlist_uuid=wishlist.uuid,
            name=command.name,
            quantity=command.quantity,
            measurement_unit=MeasurementUnit(command.measurement_unit),
            priority=Priority(command.priority),
        )
        wishlist.add_item(item)
        uow.commit()


def handle_remove_wishlist_item(command: RemoveWishlistItem, uow: AbstractUnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
        if not wishlist:
            raise WishlistNotFound(f"Wishlist {command.wishlist_uuid} not found")
        if command.item_uuid not in [item.uuid for item in wishlist.items]:
            raise WishlistItemNotFound(f"Wishlist item {command.item_uuid} not found")
        wishlist.remove_item(command.item_uuid)
        uow.commit()


WISHLIST_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateWishlist: handle_create_wishlist,
    ChangeWishlistName: handle_change_wishlist_name,
    AddWishlistItem: handle_add_wishlist_item,
    RemoveWishlistItem: handle_remove_wishlist_item,
}

WISHLIST_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    WishlistCreated: [],
    WishlistNameChanged: [],
    WishlistItemAdded: [],
    WishlistItemRemoved: [],
}
