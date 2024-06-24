from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

from src.users.domain.commands import CreateUser

auth_router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class CreateUserResponse(BaseModel):
    message: str


@auth_router.post("/register", response_model=CreateUserResponse)
def register(command: CreateUserRequest, request: Request):
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
