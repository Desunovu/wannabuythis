from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from src.common.adapters.dependencies import DefaultPasswordHasher, JWTManager
from src.users.domain.commands import CreateUser
from src.users.service.user_auth_service import generate_token

auth_router = APIRouter()


class LoginUserRequest(BaseModel):
    username: str
    password: str


class LoginUserResponse(BaseModel):
    token: str


class CreateUserResponse(BaseModel):
    message: str


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


@auth_router.post("/login", response_model=LoginUserResponse)
def login(user_data: LoginUserRequest, request: Request):
    try:
        token = generate_token(
            username=user_data.username,
            password=user_data.password,
            password_manager=DefaultPasswordHasher(),
            token_manager=JWTManager(),
            uow=request.app.state.messagebus.uow,
        )
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    return {"token": token}
