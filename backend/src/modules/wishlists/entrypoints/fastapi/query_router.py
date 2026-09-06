from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject_sync
from fastapi import APIRouter
from sqlalchemy.orm import Session

from src.infrastructure.entrypoints.fastapi.dependencies import CurrentUserDependency
from src.modules.wishlists.entrypoints.fastapi.schemas import WishlistResponse
from src.modules.wishlists.queries import wishlist_queries

wishlists_query_router = APIRouter(prefix="/wishlists", tags=["wishlist_queries"])


@wishlists_query_router.get("/")
@inject_sync
def get_current_user_wishlists(
    current_user: CurrentUserDependency,
    session: FromDishka[Session],  # сессия с гарантированным close()
) -> list[WishlistResponse]:
    wishlists = wishlist_queries.get_wishlists_owned_by(
        session=session, username=current_user.username
    )
    return [WishlistResponse.from_dataclass(wishlist) for wishlist in wishlists]


@wishlists_query_router.get("/{uuid}")
@inject_sync
def get_wishlist(uuid: UUID, session: FromDishka[Session]) -> WishlistResponse:
    wishlist = wishlist_queries.get_wishlist_by_uuid(session=session, uuid=uuid)

    return WishlistResponse.from_dataclass(wishlist)


@wishlists_query_router.get("/user/{username}")
@inject_sync
def get_wishlists_by_user(
    username: str, session: FromDishka[Session]
) -> list[WishlistResponse]:
    wishlists = wishlist_queries.get_wishlists_owned_by(
        session=session, username=username
    )

    return [WishlistResponse.from_dataclass(wishlist) for wishlist in wishlists]
