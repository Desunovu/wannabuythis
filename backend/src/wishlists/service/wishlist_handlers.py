from src.common.adapters.dependencies import UUIDGenerator
from src.common.domain.commands import Command
from src.common.domain.events import DomainEvent
from src.common.service.exceptions import (
    WishlistNotFound,
    UserNotFound,
    WishlistItemNotFound,
    WishlistAlreadyArchived,
    WishlistNotArchived,
)
from src.common.service.uow import UnitOfWork
from src.wishlists.domain.commands import (
    CreateWishlist,
    ChangeWishlistName,
    AddWishlistItem,
    RemoveWishlistItem,
    SetWishlistItemStatus,
    ArchiveWishlist,
    UnarchiveWishlist,
)
from src.wishlists.domain.events import (
    WishlistNameChanged,
    WishlistCreated,
    WishlistItemAdded,
    WishlistItemRemoved,
    WishlistItemMarkedAsNotPurchased,
    WishlistItemMarkedAsPurchased,
    WishlistArchived,
    WishlistUnarchived,
)
from src.wishlists.domain.model import Wishlist, MeasurementUnit, Priority, WishlistItem


def handle_create_wishlist(
    command: CreateWishlist,
    uow: UnitOfWork,
    uuid_generator: UUIDGenerator,
):
    with uow:
        user = uow.user_repository.get(command.owner_username)
        if not user:
            raise UserNotFound(command.owner_username)
        wishlist = Wishlist(
            uuid=uuid_generator.generate(),
            owner_username=command.owner_username,
            name=command.name,
            items=[],
        )
        uow.wishlist_repository.add(wishlist)
        wishlist.add_event(WishlistCreated(wishlist.uuid, wishlist.name))
        uow.commit()


def handle_change_wishlist_name(command: ChangeWishlistName, uow: UnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.uuid)
        if not wishlist:
            raise WishlistNotFound(command.uuid)
        wishlist.change_name(command.new_name)
        wishlist.add_event(WishlistNameChanged(wishlist.uuid, wishlist.name))
        uow.commit()


def handle_add_wishlist_item(
    command: AddWishlistItem,
    uow: UnitOfWork,
    uuid_generator: UUIDGenerator,
):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
        if not wishlist:
            raise WishlistNotFound(command.wishlist_uuid)
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


def handle_remove_wishlist_item(command: RemoveWishlistItem, uow: UnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
        if not wishlist:
            raise WishlistNotFound(command.wishlist_uuid)
        if command.item_uuid not in [item.uuid for item in wishlist.items]:
            raise WishlistItemNotFound(command.item_uuid)
        wishlist.remove_item(command.item_uuid)
        uow.commit()


def handle_set_wishlist_item_status(command: SetWishlistItemStatus, uow: UnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
        if not wishlist:
            raise WishlistNotFound(command.wishlist_uuid)
        if command.item_uuid not in [item.uuid for item in wishlist.items]:
            raise WishlistItemNotFound(command.wishlist_uuid)
        wishlist.set_item_status(command.item_uuid, command.is_purchased)
        uow.commit()


def handle_archive_wishlist(command: ArchiveWishlist, uow: UnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.uuid)
        if not wishlist:
            raise WishlistNotFound(command.uuid)
        if wishlist.is_archived:
            raise WishlistAlreadyArchived(command.uuid)
        wishlist.archive()
        uow.commit()


def handle_unarchive_wishlist(command: UnarchiveWishlist, uow: UnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.uuid)
        if not wishlist:
            raise WishlistNotFound(command.uuid)
        if not wishlist.is_archived:
            raise WishlistNotArchived(command.uuid)
        wishlist.unarchive()
        uow.commit()


WISHLIST_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateWishlist: handle_create_wishlist,
    ChangeWishlistName: handle_change_wishlist_name,
    AddWishlistItem: handle_add_wishlist_item,
    RemoveWishlistItem: handle_remove_wishlist_item,
    SetWishlistItemStatus: handle_set_wishlist_item_status,
    ArchiveWishlist: handle_archive_wishlist,
    UnarchiveWishlist: handle_unarchive_wishlist,
}

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
