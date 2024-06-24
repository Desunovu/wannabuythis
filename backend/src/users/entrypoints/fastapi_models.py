from pydantic import BaseModel


class LoginUserRequest(BaseModel):
    username: str
    password: str


class LoginUserResponse(BaseModel):
    token: str


class CreateUserResponse(BaseModel):
    message: str
