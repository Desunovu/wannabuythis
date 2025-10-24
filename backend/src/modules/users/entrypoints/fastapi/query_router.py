from dataclasses import asdict

from fastapi import APIRouter
from starlette.requests import Request

from src.core.entrypoints.fastapi_dependencies import CurrentUserDependency
from src.core.entrypoints.fastapi_limiter import limiter
from src.modules.users.entrypoints.fastapi._pydantic_models import UserResponse, PublicUserResponse
from src.modules.users.queries import user_queries

users_query_router = APIRouter(prefix="/users", tags=["user_queries"])


@users_query_router.get(
    "/me", response_model=UserResponse
)
def get_me(request: Request, current_user: CurrentUserDependency):
    return UserResponse(**asdict(current_user))


@limiter.limit("5/minute")
@users_query_router.get("/", response_model=list[PublicUserResponse])
def get_users(request: Request):
    session = request.app.state.messagebus.uow.session_factory()
    users = user_queries.get_all_users(session=session)

    return [PublicUserResponse(**asdict(user)) for user in users]


@limiter.limit("5/minute")
@users_query_router.get("/{username}", response_model=PublicUserResponse)
def get_user(
    username: str,
    request: Request,
):
    session = request.app.state.messagebus.uow.session_factory()
    user = user_queries.get_user_by_username(session=session, username=username)

    return PublicUserResponse(**asdict(user))
