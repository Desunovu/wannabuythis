from dataclasses import asdict

from dishka.integrations.fastapi import FromDishka, inject_sync
from fastapi import APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.infrastructure.entrypoints.fastapi.dependencies import CurrentUserDependency
from src.infrastructure.entrypoints.fastapi.limiter import limiter
from src.modules.users.entrypoints.fastapi.schemas import (
    PublicUserResponse,
    UserResponse,
)
from src.modules.users.queries import user_queries

users_query_router = APIRouter(prefix="/users", tags=["user_queries"])


@users_query_router.get("/me", response_model=UserResponse)
@limiter.limit("120/minute")
@inject_sync
def get_me(request: Request, current_user: CurrentUserDependency):
    return UserResponse(**asdict(current_user))


@users_query_router.get("/", response_model=list[PublicUserResponse])
@limiter.limit("60/minute")
@inject_sync
def get_users(request: Request, session: FromDishka[Session]):
    users = user_queries.get_all_users(session=session)

    return [PublicUserResponse(**asdict(user)) for user in users]


@users_query_router.get("/{username}", response_model=PublicUserResponse)
@limiter.limit("60/minute")
@inject_sync
def get_user(
    request: Request,
    username: str,
    session: FromDishka[Session],
):
    user = user_queries.get_user_by_username(session=session, username=username)

    return PublicUserResponse(**asdict(user))
