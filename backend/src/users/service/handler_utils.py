from src.common.adapters.activation_code_storage import ActivationCodeStorage
from src.common.utils.activation_code_generator import ActivationCodeGenerator
from src.common.utils.notificator import Notificator
from src.common.utils.password_manager import PasswordManager
from src.users.domain.model import User


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


def change_user_password(
    user: User, password_manager: PasswordManager, new_password: str
):
    password_manager.assert_password_valid(new_password)
    new_password_hash = password_manager.hash_password(new_password)
    user.change_password_hash(new_password_hash)
