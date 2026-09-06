from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject_sync
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from src.modules.users.domain.model import User
from src.modules.users.queries import user_queries
from src.modules.wishlists.queries import wishlist_queries
from src.shared.application.exceptions import UserNotAuthorized
from src.shared.utils.auth.token_manager import TokenManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@inject_sync
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_manager: FromDishka[TokenManager],
    session: FromDishka[Session],
) -> "User":
    username = token_manager.get_username_from_token(token)

    return user_queries.get_user_by_username(session=session, username=username)


CurrentUserDependency = Annotated[User, Depends(get_current_user)]


@inject_sync
def get_wishlist_owner(
    current_user: CurrentUserDependency,
    session: FromDishka[Session],
    request: Request,
) -> User:
    wishlist_uuid = UUID(request.path_params["wishlist_uuid"])
    wishlist = wishlist_queries.get_wishlist_by_uuid(
        session=session, uuid=wishlist_uuid
    )
    if current_user.username != wishlist.owner_username:
        raise UserNotAuthorized(username=current_user.username)
    return current_user


WishlistOwnerDependency = Annotated[User, Depends(get_wishlist_owner)]


def get_superuser(current_user: CurrentUserDependency) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user


CurrentAdminDependency = Annotated[User, Depends(get_superuser)]
