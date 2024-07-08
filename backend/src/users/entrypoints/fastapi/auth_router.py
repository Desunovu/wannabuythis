from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src import config
from src.common.entrypoints.fastapi_limiter import limiter
from src.users.domain.commands import (
    ActivateUserWithToken,
    CreateUser,
    GenerateAuthToken,
    ResendActivationLink,
)
from src.users.entrypoints.fastapi._pydantic_models import (
    CreateUserResponse,
    LoginUserResponse,
)

users_auth_router = APIRouter(tags=["auth"])


@users_auth_router.post("/login", response_model=LoginUserResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request):
    token_lifetime = config.get_auth_token_lifetime()
    command = GenerateAuthToken(
        username=form_data.username,
        password=form_data.password,
        token_lifetime=token_lifetime,
    )
    auth_token = request.app.state.messagebus.handle(command)
    return {"access_token": auth_token, "token_type": "bearer"}


@users_auth_router.post("/register", response_model=CreateUserResponse)
def register(command: CreateUser, request: Request):
    command = CreateUser(
        username=command.username,
        email=command.email,
        password=command.password,
    )
    request.app.state.messagebus.handle(command)
    return {"message": "User created successfully"}


@users_auth_router.get("/activate/{activation_token}", status_code=HTTP_200_OK)
def activate_user(activation_token: str, request: Request):
    request.app.state.messagebus.handle(ActivateUserWithToken(activation_token))


@users_auth_router.post("/activate/resend-activation-link", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
def resend_activation_link(command: ResendActivationLink, request: Request):
    request.app.state.messagebus.handle(command)
