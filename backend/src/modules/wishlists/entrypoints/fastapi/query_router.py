from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject_sync
from fastapi import APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.infrastructure.entrypoints.fastapi.dependencies import (
    CurrentUserDependency,
    OptionalCurrentUserDependency,
)
from src.infrastructure.entrypoints.fastapi.limiter import limiter
from src.modules.wishlists.entrypoints.fastapi.schemas import WishlistResponse
from src.modules.wishlists.queries import wishlist_queries
from src.shared.application.exceptions import WishlistNotFound

wishlists_query_router = APIRouter(prefix="/wishlists", tags=["wishlist_queries"])


@wishlists_query_router.get("/")
@limiter.limit("60/minute")
@inject_sync
def get_current_user_wishlists(
    request: Request,
    current_user: CurrentUserDependency,
    session: FromDishka[Session],
) -> list[WishlistResponse]:
    wishlists = wishlist_queries.get_wishlists_owned_by(
        session=session, username=current_user.username
    )
    return [WishlistResponse.from_dataclass(wishlist) for wishlist in wishlists]


@wishlists_query_router.get("/archived")
@limiter.limit("30/minute")
@inject_sync
def get_archived_wishlists(
    request: Request,
    current_user: CurrentUserDependency,
    session: FromDishka[Session],
) -> list[WishlistResponse]:
    wishlists = wishlist_queries.get_archived_wishlists_owned_by(
        session=session, username=current_user.username
    )
    return [WishlistResponse.from_dataclass(wishlist) for wishlist in wishlists]


@wishlists_query_router.get("/{uuid}")
@limiter.limit("120/minute")
@inject_sync
def get_wishlist(
    request: Request,
    uuid: UUID,
    current_user: OptionalCurrentUserDependency,
    session: FromDishka[Session],
) -> WishlistResponse:
    wishlist = wishlist_queries.get_wishlist_by_uuid(session=session, uuid=uuid)

    if (wishlist.is_archived or not wishlist.is_public) and (
        current_user is None or current_user.username != wishlist.owner_username
    ):
        raise WishlistNotFound(uuid)

    return WishlistResponse.from_dataclass(wishlist)


@wishlists_query_router.get("/user/{username}")
@limiter.limit("60/minute")
@inject_sync
def get_wishlists_by_user(
    request: Request, username: str, session: FromDishka[Session]
) -> list[WishlistResponse]:
    wishlists = wishlist_queries.get_wishlists_owned_by(
        session=session, username=username, public_only=True
    )

    return [WishlistResponse.from_dataclass(wishlist) for wishlist in wishlists]
