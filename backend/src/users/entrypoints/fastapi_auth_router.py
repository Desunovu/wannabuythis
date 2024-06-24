import datetime

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from src.common.entrypoints.fastapi_limiter import limiter
from src.users.domain.commands import (
    CreateUser,
    ActivateUser,
    ResendActivationLink,
    GenerateAuthToken,
)
from src.users.entrypoints.fastapi_models import (
    LoginUserRequest,
    LoginUserResponse,
    CreateUserResponse,
)

auth_router = APIRouter()


@auth_router.post("/login", response_model=LoginUserResponse)
def login(user_data: LoginUserRequest, request: Request):
    try:
        auth_token = request.app.state.messagebus.handle(
            GenerateAuthToken(
                username=user_data.username,
                password=user_data.password,
                exp_time=datetime.timedelta(
                    minutes=5
                ),  # TODO add expiration time from config
            )
        )
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    return {"token": auth_token}


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
        request.app.state.messagebus.handle(ActivateUser(activation_token))
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/activate/resend-activation-link", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
def resend_activation_link(command: ResendActivationLink, request: Request):
    try:
        request.app.state.messagebus.handle(command)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
