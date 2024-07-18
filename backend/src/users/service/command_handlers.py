from src.common.adapters.activation_code_storage import ActivationCodeStorage
from src.common.utils.activation_code_generator import ActivationCodeGenerator
from src.common.utils.notificator import Notificator
from src.common.utils.password_hash_util import PasswordHashUtil
from src.common.utils.token_manager import TokenManager
from src.common.domain.commands import Command
from src.common.service.exceptions import (
    CannotGenerateAuthToken,
    CannotResendActivationToken,
    CodeVerificationError,
    PasswordValidationError,
    PasswordVerificationError,
    UserAlreadyExists,
)
from src.common.service.uow import UnitOfWork
from src.users.domain.commands import (
    ActivateUser,
    ActivateUserWithCode,
    ChangeEmail,
    ChangePasswordWithOldPassword,
    ChangePasswordWithoutOldPassword,
    CreateUser,
    DeactivateUser,
    GenerateAuthToken,
    ResendActivationCode,
)
from src.users.domain.model import User
from src.users.service.handler_utils import (
    change_user_password,
    check_user_exists,
    send_new_activation_code,
)


def handle_create_user(
    command: CreateUser,
    uow: UnitOfWork,
    password_hash_util: PasswordHashUtil,
):
    with uow:
        if check_user_exists(username=command.username, uow=uow):
            raise UserAlreadyExists(command.username)
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
        raise CannotGenerateAuthToken(command.username)
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
        user.activate()
        uow.commit()


def handle_activate_user_with_code(
    command: ActivateUserWithCode,
    uow: UnitOfWork,
    activation_code_storage: ActivationCodeStorage,
):
    with uow:
        user = uow.user_repository.get(command.username)
        stored_code = activation_code_storage.get_activation_code(
            username=user.username
        )
        if stored_code is None or command.code != stored_code:
            raise CodeVerificationError

        activation_code_storage.save_activation_code(username=user.username, code="")
        user.activate()

        uow.commit()


def handle_resend_activation_code(
    command: ResendActivationCode,
    uow: UnitOfWork,
    notificator: Notificator,
    activation_code_generator: ActivationCodeGenerator,
    activation_code_storage: ActivationCodeStorage,
    password_hash_util: PasswordHashUtil,
):
    with uow:
        user = uow.user_repository.get(command.username)
    if not password_hash_util.verify_password(
        password=command.password, password_hash=user.password_hash
    ):
        raise PasswordVerificationError
    if user.is_active:
        raise CannotResendActivationToken(command.username)
    send_new_activation_code(
        user=user,
        activation_code_generator=activation_code_generator,
        activation_code_storage=activation_code_storage,
        notificator=notificator,
    )


def handle_deactivate_user(command: DeactivateUser, uow: UnitOfWork):
    with uow:
        user = uow.user_repository.get(command.username)
        user.deactivate()
        uow.commit()


USER_COMMAND_HANDLERS: dict[type[Command], callable] = {
    CreateUser: handle_create_user,
    GenerateAuthToken: handle_generate_auth_token,
    ActivateUserWithCode: handle_activate_user_with_code,
    ChangePasswordWithoutOldPassword: handle_change_password_without_old_password,
    ChangePasswordWithOldPassword: handle_change_password_with_old_password,
    ChangeEmail: handle_change_user_email,
    ActivateUser: handle_activate_user,
    ResendActivationCode: handle_resend_activation_code,
    DeactivateUser: handle_deactivate_user,
}
