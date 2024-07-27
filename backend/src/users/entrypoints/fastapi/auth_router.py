from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src import config
from src.common.entrypoints.fastapi_limiter import limiter
from src.users.domain.commands import (
    ActivateUserWithCode,
    CreateUser,
    GenerateAuthToken,
    ResendActivationCode,
)
from src.users.entrypoints.fastapi._pydantic_models import (
    ActivateUserWithCodeRequest,
    LoginUserResponse,
)

users_auth_router = APIRouter(prefix="/auth", tags=["auth"])


@users_auth_router.post("/register", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
def register(
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    request: Request,
):
    command = CreateUser(
        username=username,
        email=email,
        password=password,
    )

    request.app.state.messagebus.handle(command)


@users_auth_router.post("/login", response_model=LoginUserResponse)
@limiter.limit("5/minute")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request):
    command = GenerateAuthToken(
        username=form_data.username,
        password=form_data.password,
        token_lifetime=config.get_auth_token_lifetime(),
    )
    auth_token = request.app.state.messagebus.handle(command)

    return {"access_token": auth_token, "token_type": "bearer"}


@users_auth_router.post("/activate", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
def activate_user(body_data: ActivateUserWithCodeRequest, request: Request):
    command = ActivateUserWithCode(username=body_data.username, code=body_data.code)
    request.app.state.messagebus.handle(command)


@users_auth_router.post("/resend-activation", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
def resend_activation_code(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
):
    command = ResendActivationCode(
        username=form_data.username, password=form_data.password
    )
    request.app.state.messagebus.handle(command)
