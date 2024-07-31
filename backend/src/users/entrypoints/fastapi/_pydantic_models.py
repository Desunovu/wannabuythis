from pydantic import BaseModel


class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str
    email: str
    is_active: bool
    is_active: bool


class ResendActivationCodeRequest(BaseModel):
    username: str
    password: str


class ActivateUserWithCodeRequest(BaseModel):
    username: str
    code: str


class ChangePasswordByUserRequest(BaseModel):
    old_password: str
    new_password: str


class ChangeEmailRequest(BaseModel):
    new_email: str


class ChangePasswordWithoutOldPasswordRequest(BaseModel):
    new_password: str
