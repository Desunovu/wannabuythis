from dishka import FromDishka
from dishka.integrations.fastapi import inject_sync
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.infrastructure.entrypoints.fastapi.dependencies import CurrentAdminDependency
from src.modules.users.domain.commands import (
    ActivateUser,
    ChangeEmail,
    ChangePasswordWithoutOldPassword,
    DeactivateUser,
)
from src.modules.users.entrypoints.fastapi.schemas import (
    ChangeEmailRequest,
    ChangePasswordWithoutOldPasswordRequest,
)
from src.shared.application.mediator import Mediator

users_admin_router = APIRouter(prefix="/admin/users", tags=["admin_user_commands"])


@users_admin_router.patch("/{username}/activate", status_code=HTTP_200_OK)
@inject_sync
def activate_user(
    username: str,
    _admin: CurrentAdminDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(ActivateUser(username=username))


@users_admin_router.patch("/{username}/deactivate", status_code=HTTP_200_OK)
@inject_sync
def deactivate_user(
    username: str,
    _admin: CurrentAdminDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(DeactivateUser(username=username))


@users_admin_router.patch("/{username}/password", status_code=HTTP_200_OK)
@inject_sync
def change_password(
    username: str,
    password_data: ChangePasswordWithoutOldPasswordRequest,
    _admin: CurrentAdminDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        ChangePasswordWithoutOldPassword(
            username=username, new_password=password_data.new_password
        )
    )


@users_admin_router.patch("/{username}/email", status_code=HTTP_200_OK)
@inject_sync
def change_email(
    username: str,
    email_data: ChangeEmailRequest,
    _admin: CurrentAdminDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        ChangeEmail(
            username=username,
            new_email=email_data.new_email,
        )
    )
