from dishka import FromDishka
from dishka.integrations.fastapi import inject_sync
from fastapi import APIRouter
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED

from src.infrastructure.entrypoints.fastapi.dependencies import CurrentUserDependency
from src.infrastructure.entrypoints.fastapi.limiter import limiter
from src.modules.users.domain.commands import (
    ChangePasswordWithOldPassword,
    ConfirmEmailChange,
    RequestEmailChange,
)
from src.modules.users.entrypoints.fastapi.schemas import (
    ChangeEmailRequest,
    ChangePasswordByUserRequest,
    ConfirmEmailChangeRequest,
)
from src.shared.application.mediator import Mediator

users_command_router = APIRouter(prefix="/users/me", tags=["user_commands"])


@users_command_router.patch("/password", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
@inject_sync
def change_password(
    request: Request,
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


@users_command_router.patch("/email", status_code=HTTP_202_ACCEPTED)
@limiter.limit("5/minute")
@inject_sync
def request_email_change(
    request: Request,
    email_data: ChangeEmailRequest,
    current_user: CurrentUserDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        RequestEmailChange(
            username=current_user.username,
            new_email=email_data.new_email,
        )
    )


@users_command_router.post("/email/confirm", status_code=HTTP_200_OK)
@limiter.limit("5/minute")
@inject_sync
def confirm_email_change(
    request: Request,
    email_data: ConfirmEmailChangeRequest,
    current_user: CurrentUserDependency,
    mediator: FromDishka[Mediator],
):
    mediator.handle(
        ConfirmEmailChange(
            username=current_user.username,
            code=email_data.code,
        )
    )
