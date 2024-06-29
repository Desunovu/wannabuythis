from fastapi import APIRouter
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src.common.entrypoints.fastapi_dependencies import CurrentAdminDependency
from src.users.domain.commands import (
    ActivateUser,
    DeactivateUser,
    ChangePassword,
    ChangeEmail,
    AddRoleToUser,
    RemoveRoleFromUser,
)
from src.users.entrypoints.fastapi._pydantic_models import (
    ChangePasswordByAdminRequest,
    ChangeEmailByAdminRequest,
)

users_admin_router = APIRouter(
    prefix="/admin/users", tags=["admin_user_commands"]
)


@users_admin_router.post("/activate", status_code=HTTP_200_OK)
def activate_user(
    command: ActivateUser,
    _admin: CurrentAdminDependency,
    request: Request,
):
    request.app.state.messagebus.handle(command)


@users_admin_router.post("/deactivate", status_code=HTTP_200_OK)
def deactivate_user(
    command: DeactivateUser,
    _admin: CurrentAdminDependency,
    request: Request,
):
    request.app.state.messagebus.handle(command)


@users_admin_router.post("/change-password", status_code=HTTP_200_OK)
def change_password(
    password_data: ChangePasswordByAdminRequest,
    _admin: CurrentAdminDependency,
    request: Request,
):
    command = ChangePassword(
        username=password_data.username,
        new_password=password_data.new_password,
        called_by_admin=True,
    )

    request.app.state.messagebus.handle(command)


@users_admin_router.post("/change-email", status_code=HTTP_200_OK)
def change_email(
    email_data: ChangeEmailByAdminRequest,
    _admin: CurrentAdminDependency,
    request: Request,
):
    command = ChangeEmail(
        username=email_data.username,
        new_email=email_data.new_email,
    )

    request.app.state.messagebus.handle(command)


@users_admin_router.post("/add-role", status_code=HTTP_200_OK)
def add_role(
    command: AddRoleToUser,
    _admin: CurrentAdminDependency,
    request: Request,
):
    request.app.state.messagebus.handle(command)


@users_admin_router.post("/remove-role", status_code=HTTP_200_OK)
def remove_role(
    command: RemoveRoleFromUser,
    _admin: CurrentAdminDependency,
    request: Request,
):
    request.app.state.messagebus.handle(command)
