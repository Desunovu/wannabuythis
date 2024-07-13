from uuid import UUID

from fastapi import APIRouter
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src.common.entrypoints.fastapi_dependencies import (
    CurrentUserDependency,
    WishlistOwnerDependency,
)
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
from src.wishlists.entrypoints.fastapi._pydantic_models import (
    AddWishlistItemRequest,
    ChangeWishlistNameRequest,
    CreateWishlistRequest,
    RemoveWishlistItemRequest,
    SetWishlistItemStatusRequest,
)

wishlists_command_router = APIRouter(prefix="/wishlists", tags=["wishlist_commands"])


@wishlists_command_router.post("/create", status_code=HTTP_200_OK)
def create_wishlist(
    wishlist_data: CreateWishlistRequest,
    current_user: CurrentUserDependency,
    request: Request,
):
    command = CreateWishlist(
        owner_username=current_user.username,
        name=wishlist_data.wishlist_name,
    )
    request.app.state.messagebus.handle(command)


@wishlists_command_router.post("/change-name/{wishlist_uuid}", status_code=HTTP_200_OK)
def change_wishlist_name(
    wishlist_uuid: UUID,
    wishlist_data: ChangeWishlistNameRequest,
    _wishlist_owner: WishlistOwnerDependency,
    request: Request,
):
    command = ChangeWishlistName(uuid=wishlist_uuid, new_name=wishlist_data.new_name)
    request.app.state.messagebus.handle(command)


@wishlists_command_router.post("/archive/{wishlist_uuid}", status_code=HTTP_200_OK)
def archive_wishlist(
    wishlist_uuid: UUID,
    _wishlist_owner: WishlistOwnerDependency,
    request: Request,
):
    command = ArchiveWishlist(uuid=wishlist_uuid)
    request.app.state.messagebus.handle(command)


@wishlists_command_router.post("/unarchive/{wishlist_uuid}", status_code=HTTP_200_OK)
def unarchive_wishlist(
    wishlist_uuid: UUID,
    _wishlist_owner: WishlistOwnerDependency,
    request: Request,
):
    command = UnarchiveWishlist(uuid=wishlist_uuid)
    request.app.state.messagebus.handle(command)


@wishlists_command_router.post("/add-item/{wishlist_uuid}", status_code=HTTP_200_OK)
def add_wishlist_item(
    wishlist_uuid: UUID,
    item_data: AddWishlistItemRequest,
    _wishlist_owner: WishlistOwnerDependency,
    request: Request,
):
    command = AddWishlistItem(wishlist_uuid=wishlist_uuid, **item_data.model_dump())
    request.app.state.messagebus.handle(command)


@wishlists_command_router.post("/remove-item/{wishlist_uuid}")
def remove_wishlist_item(
    wishlist_uuid: UUID,
    item_data: RemoveWishlistItemRequest,
    _wishlist_owner: WishlistOwnerDependency,
    request: Request,
):
    command = RemoveWishlistItem(
        wishlist_uuid=wishlist_uuid, item_uuid=item_data.item_uuid
    )
    request.app.state.messagebus.handle(command)


@wishlists_command_router.post("/mark-item-as-purchased/{wishlist_uuid}")
def set_wishlist_item_status(
    wishlist_uuid: UUID,
    item_data: SetWishlistItemStatusRequest,
    _wishlist_owner: WishlistOwnerDependency,
    request: Request,
):
    command = MarkWishlistItemAsPurchased(
        wishlist_uuid=wishlist_uuid,
        item_uuid=item_data.item_uuid,
    )
    request.app.state.messagebus.handle(command)


@wishlists_command_router.post("/mark-item-as-not-purchased/{wishlist_uuid}")
def set_wishlist_item_status(
    wishlist_uuid: UUID,
    item_data: SetWishlistItemStatusRequest,
    _wishlist_owner: WishlistOwnerDependency,
    request: Request,
):
    command = MarkWishlistItemAsNotPurchased(
        wishlist_uuid=wishlist_uuid,
        item_uuid=item_data.item_uuid,
    )
    request.app.state.messagebus.handle(command)
