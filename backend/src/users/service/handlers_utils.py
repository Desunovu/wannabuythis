from src.common.adapters.activation_code_storage import ActivationCodeStorage
from src.common.utils.activation_code_generator import ActivationCodeGenerator
from src.common.utils.notificator import Notificator
from src.common.service.exceptions import PasswordValidationError, UserNotFound
from src.common.service.uow import UnitOfWork
from src.users.domain.model import User


def check_user_exists(username: str, uow: UnitOfWork) -> bool:
    try:
        _user = uow.user_repository.get(username)
        return True
    except UserNotFound:
        return False


def send_new_activation_code(
    user: User,
    activation_code_generator: ActivationCodeGenerator,
    activation_code_storage: ActivationCodeStorage,
    notificator: Notificator,
):
    activation_code = activation_code_generator.create_code()
    activation_code_storage.save_activation_code(
        username=user.username, code=activation_code
    )
    notificator.send_activation_code(recipient=user, activation_code=activation_code)


def change_user_password(user, new_password, password_hash_util):
    if not User.validate_password(new_password):
        raise PasswordValidationError
    new_password_hash = password_hash_util.hash_password(new_password)
    user.change_password_hash(new_password_hash)
