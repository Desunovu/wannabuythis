from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from src.common.dependencies.token_manager import TokenManager
from src.users.queries import user_queries

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


def get_current_admin(
    current_user: CurrentUserDependency,
):
    admin_role = next(
        (role for role in current_user.roles if role.name == "admin"),
        None
    )
    if not admin_role:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    return current_user


CurrentAdminDependency = Annotated["User", Depends(get_current_admin)]
