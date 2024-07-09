from fastapi import APIRouter
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from src.common.entrypoints.fastapi_dependencies import CurrentUserDependency
from src.users.domain.commands import ChangeEmail, ChangePasswordWithOldPassword
from src.users.entrypoints.fastapi._pydantic_models import (
    ChangeEmailByUserRequest,
    ChangePasswordByUserRequest,
)

users_command_router = APIRouter(prefix="/users", tags=["user_commands"])


@users_command_router.post("/change-password", status_code=HTTP_200_OK)
def change_password(
    password_data: ChangePasswordByUserRequest,
    current_user: CurrentUserDependency,
    request: Request,
):
    command = ChangePasswordWithOldPassword(
        username=current_user.username,
        new_password=password_data.new_password,
        old_password=password_data.old_password,
    )
    request.app.state.messagebus.handle(command)


@users_command_router.post("/change-email", status_code=HTTP_200_OK)
def change_email(
    email_data: ChangeEmailByUserRequest,
    current_user: CurrentUserDependency,
    request: Request,
):
    command = ChangeEmail(
        username=current_user.username,
        new_email=email_data.new_email,
    )
    request.app.state.messagebus.handle(command)
