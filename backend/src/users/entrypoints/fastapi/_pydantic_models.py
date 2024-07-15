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
    is_active: bool


class ActivateUserWithCodeRequest(BaseModel):
    username: str
    code: str


class ChangePasswordByUserRequest(BaseModel):
    old_password: str
    new_password: str


class ChangeEmailByUserRequest(BaseModel):
    new_email: str


class ChangePasswordByAdminRequest(BaseModel):
    username: str
    new_password: str


class ChangeEmailByAdminRequest(BaseModel):
    username: str
    new_email: str
