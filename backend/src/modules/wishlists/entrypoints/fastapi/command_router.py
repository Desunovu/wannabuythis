from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject_sync
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.infrastructure.entrypoints.fastapi.dependencies import (
    CurrentUserDependency,
    WishlistOwnerDependency,
)
from src.modules.wishlists.domain.commands import (
    AddWishlistItem,
    ArchiveWishlist,
    ChangeWishlistName,
    CreateWishlist,
    MarkWishlistItemAsNotPurchased,
    MarkWishlistItemAsPurchased,
    RemoveWishlistItem,
    UnarchiveWishlist,
)
from src.modules.wishlists.entrypoints.fastapi.schemas import (
    AddWishlistItemRequest,
    ChangeWishlistNameRequest,
    CreateWishlistRequest,
    RemoveWishlistItemRequest,
    SetWishlistItemStatusRequest,
)
from src.shared.application.mediator import Mediator

wishlists_command_router = APIRouter(prefix="/wishlists", tags=["wishlist_commands"])


@wishlists_command_router.post("/create", status_code=HTTP_200_OK)
@inject_sync
def create_wishlist(
    wishlist_data: CreateWishlistRequest,
    current_user: CurrentUserDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        CreateWishlist(
            owner_username=current_user.username,
            name=wishlist_data.wishlist_name,
        )
    )


@wishlists_command_router.post("/change-name/{wishlist_uuid}", status_code=HTTP_200_OK)
@inject_sync
def change_wishlist_name(
    wishlist_uuid: UUID,
    wishlist_data: ChangeWishlistNameRequest,
    _wishlist_owner: WishlistOwnerDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        ChangeWishlistName(uuid=wishlist_uuid, new_name=wishlist_data.new_name)
    )


@wishlists_command_router.post("/archive/{wishlist_uuid}", status_code=HTTP_200_OK)
@inject_sync
def archive_wishlist(
    wishlist_uuid: UUID,
    _wishlist_owner: WishlistOwnerDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(ArchiveWishlist(uuid=wishlist_uuid))


@wishlists_command_router.post("/unarchive/{wishlist_uuid}", status_code=HTTP_200_OK)
@inject_sync
def unarchive_wishlist(
    wishlist_uuid: UUID,
    _wishlist_owner: WishlistOwnerDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(UnarchiveWishlist(uuid=wishlist_uuid))


@wishlists_command_router.post("/add-item/{wishlist_uuid}", status_code=HTTP_200_OK)
@inject_sync
def add_wishlist_item(
    wishlist_uuid: UUID,
    item_data: AddWishlistItemRequest,
    _wishlist_owner: WishlistOwnerDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        AddWishlistItem(wishlist_uuid=wishlist_uuid, **item_data.model_dump())
    )


@wishlists_command_router.post("/remove-item/{wishlist_uuid}")
@inject_sync
def remove_wishlist_item(
    wishlist_uuid: UUID,
    item_data: RemoveWishlistItemRequest,
    _wishlist_owner: WishlistOwnerDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        RemoveWishlistItem(wishlist_uuid=wishlist_uuid, item_uuid=item_data.item_uuid)
    )


@wishlists_command_router.post("/mark-item-as-purchased/{wishlist_uuid}")
@inject_sync
def mark_item_as_purchased(
    wishlist_uuid: UUID,
    item_data: SetWishlistItemStatusRequest,
    _wishlist_owner: WishlistOwnerDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        MarkWishlistItemAsPurchased(
            wishlist_uuid=wishlist_uuid,
            item_uuid=item_data.item_uuid,
        )
    )


@wishlists_command_router.post("/mark-item-as-not-purchased/{wishlist_uuid}")
@inject_sync
def mark_item_as_not_purchased(
    wishlist_uuid: UUID,
    item_data: SetWishlistItemStatusRequest,
    _wishlist_owner: WishlistOwnerDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        MarkWishlistItemAsNotPurchased(
            wishlist_uuid=wishlist_uuid,
            item_uuid=item_data.item_uuid,
        )
    )
