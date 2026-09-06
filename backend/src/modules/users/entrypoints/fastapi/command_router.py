from dishka import FromDishka
from dishka.integrations.fastapi import inject_sync
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from src.infrastructure.entrypoints.fastapi.dependencies import CurrentUserDependency
from src.modules.users.domain.commands import ChangeEmail, ChangePasswordWithOldPassword
from src.modules.users.entrypoints.fastapi.schemas import (
    ChangeEmailRequest,
    ChangePasswordByUserRequest,
)
from src.shared.application.mediator import Mediator

users_command_router = APIRouter(prefix="/users/me", tags=["user_commands"])


@users_command_router.patch("/password", status_code=HTTP_200_OK)
@inject_sync
def change_password(
    password_data: ChangePasswordByUserRequest,
    current_user: CurrentUserDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        ChangePasswordWithOldPassword(
            username=current_user.username,
            new_password=password_data.new_password,
            old_password=password_data.old_password,
        )
    )


@users_command_router.patch("/email", status_code=HTTP_200_OK)
@inject_sync
def change_email(
    email_data: ChangeEmailRequest,
    current_user: CurrentUserDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        ChangeEmail(
            username=current_user.username,
            new_email=email_data.new_email,
        )
    )
