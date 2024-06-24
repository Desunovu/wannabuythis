from src.common.adapters.dependencies import PasswordHashUtil, Notificator, TokenManager
from src.common.domain.commands import Command
from src.common.service.exceptions import (
    UserNotFound,
    UserExists,
    PasswordValidationError,
    PasswordVerificationError,
    UserAlreadyDeactivated,
    UserAlreadyActive,
    RoleNotFound,
    UserDoesNotHaveRole,
    UserAlreadyHasRole,
    UserNotActive,
)
from src.common.service.uow import UnitOfWork
from src.users.domain.commands import (
    CreateUser,
    ChangePassword,
    DeactivateUser,
    ActivateUser,
    ChangeEmail,
    AddRoleToUser,
    RemoveRoleFromUser,
    ResendActivationLink,
    GenerateAuthToken,
    ActivateUserWithToken,
)
from src.users.domain.events import (
    PasswordChanged,
)
from src.users.domain.model import User
from src.users.service.handlers_utils import check_user_exists


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
        user = User(command.username, command.email, password_hash)
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
    if not user:
        raise UserNotFound(username=command.username)
    if not user.is_active:
        raise UserNotActive(username=command.username)
    if not password_hash_util.verify_password(
        password=command.password, password_hash=user.password_hash
    ):
        raise PasswordVerificationError

    token = token_manager.generate_token(
        username=user.username, exp_time=command.exp_time
    )

    return token


def handle_change_password(
    command: ChangePassword,
    uow: UnitOfWork,
    password_hash_util: PasswordHashUtil,
):
    with uow:
        user = uow.user_repository.get(command.username)
        if not user:
            raise UserNotFound(command.username)
        if not User.validate_password(command.new_password):
            raise PasswordValidationError()
        if not command.called_by_admin:
            if not password_hash_util.verify_password(
                password=command.old_password, password_hash=user.password_hash
            ):
                raise PasswordVerificationError()
        new_password_hash = password_hash_util.hash_password(command.new_password)
        user.change_password_hash(new_password_hash)
        user.add_event(PasswordChanged(user.username))
        uow.commit()


def handle_change_user_email(command: ChangeEmail, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(command.username)
        if not user:
            raise UserNotFound(command.username)
        user.change_email(command.new_email)
        uow.commit()


def handle_activate_user(command: ActivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(command.username)
        if not user:
            raise UserNotFound(command.username)
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
        if not user:
            raise UserNotFound(username)
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
        if not user:
            raise UserNotFound(command.username)
        if not password_hash_util.verify_password(
            password=command.password, password_hash=user.password_hash
        ):
            raise PasswordVerificationError
        if user.is_active:
            raise UserAlreadyActive(command.username)
        # TODO set activation token expiration time from config
        # TODO maybe dry this code, because it's similar to the handle_user_created
        activation_token = token_manager.generate_token(
            username=user.username, exp_time=None
        )
        notificator.send_activation_link(
            recipient=user, activation_token=activation_token
        )


def handle_deactivate_user(command: DeactivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(command.username)
        if not user:
            raise UserNotFound(command.username)
        if not user.is_active:
            raise UserAlreadyDeactivated(command.username)
        user.deactivate()
        uow.commit()


def handle_add_role_to_user(command: AddRoleToUser, uow: UnitOfWork):
    with uow:
        role = uow.role_repository.get(command.role_name)
        if not role:
            raise RoleNotFound(command.role_name)
        user = uow.user_repository.get(command.username)
        if not user:
            raise UserNotFound(command.username)
        if user.has_role(role):
            raise UserAlreadyHasRole(command.username, command.role_name)
        user.add_role(role)
        uow.commit()


def handle_remove_role_from_user(command: RemoveRoleFromUser, uow: UnitOfWork):
    with uow:
        role = uow.role_repository.get(command.role_name)
        if not role:
            raise RoleNotFound(command.role_name)
        user = uow.user_repository.get(command.username)
        if not user:
            raise UserNotFound(command.username)
        if not user.has_role(role):
            raise UserDoesNotHaveRole(command.username, command.role_name)
        user.remove_role(role)
        uow.commit()


USER_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateUser: handle_create_user,
    GenerateAuthToken: handle_generate_auth_token,
    ActivateUserWithToken: handle_activate_user_with_token,
    ChangePassword: handle_change_password,
    ChangeEmail: handle_change_user_email,
    ActivateUser: handle_activate_user,
    ResendActivationLink: handle_resend_activation_link,
    DeactivateUser: handle_deactivate_user,
    AddRoleToUser: handle_add_role_to_user,
    RemoveRoleFromUser: handle_remove_role_from_user,
}
