from pydantic import BaseModel, EmailStr, Field


class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str
    email: str
    is_active: bool
    is_superuser: bool


class PublicUserResponse(BaseModel):
    username: str


class ResendActivationCodeRequest(BaseModel):
    username: str
    password: str


class ActivateUserWithCodeRequest(BaseModel):
    username: str
    code: str = Field(pattern=r"^\d{8}$")


class ChangePasswordByUserRequest(BaseModel):
    old_password: str
    new_password: str


class ChangeEmailRequest(BaseModel):
    new_email: EmailStr


class ChangePasswordWithoutOldPasswordRequest(BaseModel):
    new_password: str
