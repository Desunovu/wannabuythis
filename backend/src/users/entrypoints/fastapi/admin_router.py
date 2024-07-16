from fastapi import APIRouter
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src.common.entrypoints.fastapi_dependencies import CurrentAdminDependency
from src.users.domain.commands import (
    ActivateUser,
    ChangeEmail,
    ChangePasswordWithoutOldPassword,
    DeactivateUser,
)
from src.users.entrypoints.fastapi._pydantic_models import (
    ChangeEmailRequest,
    ChangePasswordWithoutOldPasswordRequest,
)

users_admin_router = APIRouter(prefix="/admin/users", tags=["admin_user_commands"])


@users_admin_router.patch("/{username}/activate", status_code=HTTP_200_OK)
def activate_user(
    username: str,
    _admin: CurrentAdminDependency,
    request: Request,
):
    command = ActivateUser(username=username)
    request.app.state.messagebus.handle(command)


@users_admin_router.patch("/{username}/deactivate", status_code=HTTP_200_OK)
def deactivate_user(
    username: str,
    _admin: CurrentAdminDependency,
    request: Request,
):
    command = DeactivateUser(username=username)
    request.app.state.messagebus.handle(command)


@users_admin_router.patch("/{username}/password", status_code=HTTP_200_OK)
def change_password(
    username: str,
    password_data: ChangePasswordWithoutOldPasswordRequest,
    _admin: CurrentAdminDependency,
    request: Request,
):
    command = ChangePasswordWithoutOldPassword(
        username=username, new_password=password_data.new_password
    )
    request.app.state.messagebus.handle(command)


@users_admin_router.patch("/{username}/email", status_code=HTTP_200_OK)
def change_email(
    username: str,
    email_data: ChangeEmailRequest,
    _admin: CurrentAdminDependency,
    request: Request,
):
    command = ChangeEmail(
        username=username,
        new_email=email_data.new_email,
    )
    request.app.state.messagebus.handle(command)
