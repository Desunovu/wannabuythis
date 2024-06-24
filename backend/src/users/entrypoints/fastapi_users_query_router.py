from fastapi import APIRouter
from starlette.requests import Request

from src.common.entrypoints.fastapi_dependencies import CurrentUserDependency
from src.common.entrypoints.fastapi_limiter import limiter
from src.users.entrypoints.fastapi_models import UserResponse
from src.users.queries import user_queries

users_query_router = APIRouter(prefix="/users", tags=["users"])


@users_query_router.get(
    "/me",
)
def get_me(request: Request, current_user: CurrentUserDependency):
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        roles=current_user.roles,
    )


@limiter.limit("5/minute")
@users_query_router.get("/{username}")
def get_user(
    username: str,
    request: Request,
):
    session = request.app.state.messagebus.uow.session_factory()
    user = user_queries.get_user_by_username(session=session, username=username)

    return UserResponse(
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        roles=user.roles,
    )
