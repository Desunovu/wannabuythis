import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from src.common.entrypoints.fastapi_limiter import limiter
from src.users.domain.commands import (
    CreateUser,
    ResendActivationLink,
    GenerateAuthToken,
    ActivateUserWithToken,
)
from src.users.entrypoints.fastapi_models import (
    LoginUserResponse,
    CreateUserResponse,
)

auth_router = APIRouter()


@auth_router.post("/login", response_model=LoginUserResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request):
    try:
        auth_token = request.app.state.messagebus.handle(
            GenerateAuthToken(
                username=form_data.username,
                password=form_data.password,
                exp_time=datetime.timedelta(
                    minutes=5
                ),  # TODO add expiration time from config
            )
        )
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    return {"access_token": auth_token, "token_type": "bearer"}


@auth_router.post("/register", response_model=CreateUserResponse)
def register(command: CreateUser, request: Request):
    try:
        request.app.state.messagebus.handle(
            CreateUser(
                username=command.username,
                email=command.email,
                password=command.password,
            )
        )
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "User created successfully"}


@auth_router.get("/activate/{activation_token}", status_code=HTTP_200_OK)
def activate_user(activation_token: str, request: Request):
    try:
        request.app.state.messagebus.handle(ActivateUserWithToken(activation_token))
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/activate/resend-activation-link", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
def resend_activation_link(command: ResendActivationLink, request: Request):
    try:
        request.app.state.messagebus.handle(command)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
