from pydantic import BaseModel


class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str


class CreateUserResponse(BaseModel):
    message: str


class UserResponse(BaseModel):
    username: str
    email: str
    is_active: bool
    roles: list
