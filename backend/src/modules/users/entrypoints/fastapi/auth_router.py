from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject_sync
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src.config import Settings
from src.infrastructure.entrypoints.fastapi.limiter import limiter
from src.modules.users.domain.commands import (
    ActivateUserWithCode,
    CreateUser,
    GenerateAuthToken,
    ResendActivationCode,
)
from src.modules.users.entrypoints.fastapi.schemas import (
    ActivateUserWithCodeRequest,
    LoginUserResponse,
)
from src.shared.application.mediator import Mediator

users_auth_router = APIRouter(prefix="/auth", tags=["auth"])


@users_auth_router.post("/register", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
@inject_sync
def register(
    request: Request,
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        CreateUser(
            username=username,
            email=email,
            password=password,
        )
    )


@users_auth_router.post("/login", response_model=LoginUserResponse)
@limiter.limit("5/minute")
@inject_sync
def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    mediator: FromDishka[Mediator],
    settings: FromDishka[Settings],
):
    auth_token = mediator.handle(
        GenerateAuthToken(
            username=form_data.username,
            password=form_data.password,
            token_lifetime=settings.auth_token_lifetime,
        )
    )

    return {"access_token": auth_token, "token_type": "bearer"}


@users_auth_router.post("/activate", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
@inject_sync
def activate_user(
    request: Request,
    body_data: ActivateUserWithCodeRequest,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        ActivateUserWithCode(username=body_data.username, code=body_data.code)
    )


@users_auth_router.post("/resend-activation", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
@inject_sync
def resend_activation_code(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        ResendActivationCode(username=form_data.username, password=form_data.password)
    )
