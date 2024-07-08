from typing import TYPE_CHECKING, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from src.common.dependencies.token_manager import TokenManager
from src.common.service.exceptions import UserNotAuthorized
from src.users.queries import user_queries
from src.wishlists.queries import wishlist_queries

if TYPE_CHECKING:
    from src.users.domain.model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
) -> "User":
    """FastAPI dependency to get current user from token"""
    token_manager: TokenManager = request.app.state.dependencies["token_manager"]
    session = request.app.state.messagebus.uow.session_factory()

    username = token_manager.get_username_from_token(token)
    user = user_queries.get_user_by_username(session=session, username=username)

    return user


CurrentUserDependency = Annotated["User", Depends(get_current_user)]


def get_wishlist_owner(
    current_user: CurrentUserDependency,
    request: Request,
) -> "User":
    """FastAPI dependency to check if current user is wishlist owner"""
    session = request.app.state.messagebus.uow.session_factory()
    wishlist_uuid = UUID(request.path_params["wishlist_uuid"])

    wishlist = wishlist_queries.get_wishlist_by_uuid(
        session=session, uuid=wishlist_uuid
    )
    if current_user.username != wishlist.owner_username:
        raise UserNotAuthorized(username=current_user.username)

    return current_user


WishlistOwnerDependency = Annotated["User", Depends(get_wishlist_owner)]


def get_superuser(
    current_user: CurrentUserDependency,
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    return current_user


CurrentAdminDependency = Annotated["User", Depends(get_superuser)]
