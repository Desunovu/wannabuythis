from src.common.dependencies.notificator import Notificator
from src.common.dependencies.password_hash_util import PasswordHashUtil
from src.common.dependencies.token_manager import TokenManager
from src.common.domain.commands import Command
from src.common.service.exceptions import (
    PasswordValidationError,
    PasswordVerificationError,
    UserAlreadyActive,
    UserAlreadyDeactivated,
    UserExists,
    UserNotActive,
)
from src.common.service.uow import UnitOfWork
from src.users.domain.commands import (
    ActivateUser,
    ActivateUserWithToken,
    ChangeEmail,
    ChangePasswordWithOldPassword,
    ChangePasswordWithoutOldPassword,
    CreateUser,
    DeactivateUser,
    GenerateAuthToken,
    ResendActivationLink,
)
from src.users.domain.model import User
from src.users.service.handlers_utils import (
    change_user_password,
    check_user_exists,
    send_notification_with_activation_link,
)


def handle_create_user(
    command: CreateUser,
    uow: UnitOfWork,
    password_hash_util: PasswordHashUtil,
):
    with uow:
        if check_user_exists(username=command.username, uow=uow):
            raise UserExists(command.username)
        if not User.validate_password(command.password):
            raise PasswordValidationError()
        password_hash = password_hash_util.hash_password(command.password)
        user = User(
            username=command.username, email=command.email, password_hash=password_hash
        )
        uow.user_repository.add(user)
        uow.commit()


def handle_generate_auth_token(
    command: GenerateAuthToken,
    uow: UnitOfWork,
    password_hash_util: PasswordHashUtil,
    token_manager: TokenManager,
):
    with uow:
        user = uow.user_repository.get(command.username)
    if not user.is_active:
        raise UserNotActive(command.username)
    if not password_hash_util.verify_password(
        password=command.password, password_hash=user.password_hash
    ):
        raise PasswordVerificationError
    token = token_manager.generate_token(
        username=user.username, token_lifetime=command.token_lifetime
    )
    return token


def handle_change_password_without_old_password(
    command: ChangePasswordWithoutOldPassword, uow: UnitOfWork, password_hash_util
):
    with uow:
        user = uow.user_repository.get(command.username)
        change_user_password(
            user=user,
            new_password=command.new_password,
            password_hash_util=password_hash_util,
        )
        uow.commit()


def handle_change_password_with_old_password(
    command: ChangePasswordWithOldPassword,
    uow: UnitOfWork,
    password_hash_util: PasswordHashUtil,
):
    with uow:
        user = uow.user_repository.get(command.username)
        if not password_hash_util.verify_password(
            password=command.old_password, password_hash=user.password_hash
        ):
            raise PasswordVerificationError
        change_user_password(
            user=user,
            new_password=command.new_password,
            password_hash_util=password_hash_util,
        )
        uow.commit()


def handle_change_user_email(command: ChangeEmail, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(command.username)
        user.change_email(command.new_email)
        uow.commit()


def handle_activate_user(command: ActivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(command.username)
        if user.is_active:
            raise UserAlreadyActive(command.username)
        user.activate()
        uow.commit()


def handle_activate_user_with_token(
    command: ActivateUserWithToken, uow: UnitOfWork, token_manager: TokenManager
):
    username = token_manager.get_username_from_token(command.token)
    with uow:
        user = uow.user_repository.get(username)
        if user.is_active:
            raise UserAlreadyActive(username)
        user.activate()
        uow.commit()


def handle_resend_activation_link(
    command: ResendActivationLink,
    uow: UnitOfWork,
    notificator: Notificator,
    token_manager: TokenManager,
    password_hash_util: PasswordHashUtil,
):
    with uow:
        user = uow.user_repository.get(command.username)
        if not password_hash_util.verify_password(
            password=command.password, password_hash=user.password_hash
        ):
            raise PasswordVerificationError
        if user.is_active:
            raise UserAlreadyActive(command.username)
        send_notification_with_activation_link(
            notificator=notificator, token_manager=token_manager, user=user
        )


def handle_deactivate_user(command: DeactivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(command.username)
        if not user.is_active:
            raise UserAlreadyDeactivated(command.username)
        user.deactivate()
        uow.commit()


USER_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateUser: handle_create_user,
    GenerateAuthToken: handle_generate_auth_token,
    ActivateUserWithToken: handle_activate_user_with_token,
    ChangePasswordWithoutOldPassword: handle_change_password_without_old_password,
    ChangePasswordWithOldPassword: handle_change_password_with_old_password,
    ChangeEmail: handle_change_user_email,
    ActivateUser: handle_activate_user,
    ResendActivationLink: handle_resend_activation_link,
    DeactivateUser: handle_deactivate_user,
}
