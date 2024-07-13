from src.common.dependencies.uuid_generator import UUIDGenerator
from src.common.domain.commands import Command
from src.common.service.exceptions import (
    WishlistAlreadyArchived,
    WishlistItemNotFound,
    WishlistNotArchived,
)
from src.common.service.uow import UnitOfWork
from src.wishlists.domain.commands import (
    AddWishlistItem,
    ArchiveWishlist,
    ChangeWishlistName,
    CreateWishlist,
    MarkWishlistItemAsNotPurchased,
    MarkWishlistItemAsPurchased,
    RemoveWishlistItem,
    UnarchiveWishlist,
)
from src.wishlists.domain.model import MeasurementUnit, Priority, Wishlist, WishlistItem


def handle_create_wishlist(
    command: CreateWishlist,
    uow: UnitOfWork,
    uuid_generator: UUIDGenerator,
):
    with uow:
        _user = uow.user_repository.get(command.owner_username)
        wishlist = Wishlist(
            uuid=uuid_generator.generate(),
            owner_username=command.owner_username,
            name=command.name,
            items=[],
        )
        uow.wishlist_repository.add(wishlist)
        uow.commit()


def handle_change_wishlist_name(command: ChangeWishlistName, uow: UnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.uuid)
        wishlist.change_name(command.new_name)
        uow.commit()


def handle_add_wishlist_item(
    command: AddWishlistItem,
    uow: UnitOfWork,
    uuid_generator: UUIDGenerator,
):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
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
        if command.item_uuid not in [item.uuid for item in wishlist.items]:
            raise WishlistItemNotFound(command.item_uuid)
        wishlist.remove_item(command.item_uuid)
        uow.commit()


def handle_mark_wishlist_item_as_purchased(
    command: MarkWishlistItemAsPurchased, uow: UnitOfWork
):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
        if command.item_uuid not in [item.uuid for item in wishlist.items]:
            raise WishlistItemNotFound(command.wishlist_uuid)
        wishlist.mark_item_as_purchased(item_uuid=command.item_uuid)
        uow.commit()


def handle_mark_wishlist_item_as_not_purchased(
    command: MarkWishlistItemAsNotPurchased, uow: UnitOfWork
):
    with uow:
        wishlist = uow.wishlist_repository.get(command.wishlist_uuid)
        if command.item_uuid not in [item.uuid for item in wishlist.items]:
            raise WishlistItemNotFound(command.wishlist_uuid)
        wishlist.mark_item_as_not_purchased(item_uuid=command.item_uuid)
        uow.commit()


def handle_archive_wishlist(command: ArchiveWishlist, uow: UnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.uuid)
        if wishlist.is_archived:
            raise WishlistAlreadyArchived(command.uuid)
        wishlist.archive()
        uow.commit()


def handle_unarchive_wishlist(command: UnarchiveWishlist, uow: UnitOfWork):
    with uow:
        wishlist = uow.wishlist_repository.get(command.uuid)
        if not wishlist.is_archived:
            raise WishlistNotArchived(command.uuid)
        wishlist.unarchive()
        uow.commit()


WISHLIST_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateWishlist: handle_create_wishlist,
    ChangeWishlistName: handle_change_wishlist_name,
    AddWishlistItem: handle_add_wishlist_item,
    RemoveWishlistItem: handle_remove_wishlist_item,
    MarkWishlistItemAsPurchased: handle_mark_wishlist_item_as_purchased,
    MarkWishlistItemAsNotPurchased: handle_mark_wishlist_item_as_not_purchased,
    ArchiveWishlist: handle_archive_wishlist,
    UnarchiveWishlist: handle_unarchive_wishlist,
}
