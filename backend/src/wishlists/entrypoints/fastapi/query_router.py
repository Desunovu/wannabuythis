from uuid import UUID

from fastapi import APIRouter
from starlette.requests import Request

from src.common.entrypoints.fastapi_dependencies import CurrentUserDependency
from src.wishlists.entrypoints.fastapi._pydantic_models import WishlistResponse
from src.wishlists.queries import wishlist_queries

wishlists_query_router = APIRouter(prefix="/wishlists", tags=["wishlist_queries"])


@wishlists_query_router.get("/{uuid}")
def get_wishlist(uuid: UUID, request: Request) -> WishlistResponse:
    session = request.app.state.messagebus.uow.session_factory()
    wishlist = wishlist_queries.get_wishlist_by_uuid(session=session, uuid=uuid)

    return WishlistResponse.from_dataclass(wishlist)


@wishlists_query_router.get("/")
def get_current_user_wishlists(
    request: Request,
    current_user: CurrentUserDependency,
) -> list[WishlistResponse]:
    session = request.app.state.messagebus.uow.session_factory()

    wishlists = wishlist_queries.get_wishlists_owned_by(
        session=session, username=current_user.username
    )

    return [WishlistResponse.from_dataclass(wishlist) for wishlist in wishlists]


@wishlists_query_router.get("/user/{username}")
def get_wishlists_by_user(username: str, request: Request) -> list[WishlistResponse]:
    session = request.app.state.messagebus.uow.session_factory()
    wishlists = wishlist_queries.get_wishlists_owned_by(
        session=session, username=username
    )

    return [WishlistResponse.from_dataclass(wishlist) for wishlist in wishlists]
