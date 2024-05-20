from uuid import uuid4

from src.domain.shared_kernel.commands import Command
from src.domain.shared_kernel.events import DomainEvent
from src.domain.wishlist.commands import (
    CreateWishlist,
    ChangeWishlistName,
    AddWishlistItem,
    RemoveWishlistItem,
)
from src.domain.wishlist.events import (
    WishlistNameChanged,
    WishlistCreated,
    WishlistItemAdded,
    WishlistItemRemoved,
)
from src.domain.wishlist.wishlist import Wishlist
from src.domain.wishlist.wishlist_item import WishlistItem, MeasurementUnit, Priority
from src.service_layer.handlers.exceptions import (
    WishlistNotFound,
    UserNotFound,
    WishlistItemNotFound,
)
from src.service_layer.unit_of_work import AbstractUnitOfWork


# TODO move uuid4 dependency to Bootstrap layer (code should depend on generate_uuid callable)


def handle_create_wishlist(command: CreateWishlist, uow: AbstractUnitOfWork):
    with uow:
        user = uow.user_repository.get(username=command.owner_username)
        if not user:
            raise UserNotFound(
                f"User {command.owner_username} not found to create wishlist"
            )
        wishlist = Wishlist(
            uuid=str(uuid4()),
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


def handle_add_wishlist_item(command: AddWishlistItem, uow: AbstractUnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
        if not wishlist:
            raise WishlistNotFound(f"Wishlist {command.wishlist_uuid} not found")
        item = WishlistItem(
            uuid=str(uuid4()),
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
