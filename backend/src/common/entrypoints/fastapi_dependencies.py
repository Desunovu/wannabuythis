from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

from src.common.adapters.dependencies import TokenManager

if TYPE_CHECKING:
    from src.users.domain.model import User
    from src.users.adapters.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    request: Request,
) -> "User":
    """FastAPI dependency to get current user from token"""
    token_manager: TokenManager = request.app.state.dependencies["token_manager"]
    user_repository: "UserRepository" = request.app.state.dependencies[
        "uow"
    ].user_repository

    username = token_manager.get_username_from_token(token)
    user = user_repository.get(username)

    return user


CurrentUserDependency = Annotated["User", Depends(get_current_user)]
