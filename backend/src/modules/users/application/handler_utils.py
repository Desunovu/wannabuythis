from src.config import settings
from src.modules.users.domain.model import User
from src.shared.application.exceptions import UserInvalidName
from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.activation_codes.activation_code_generator import (
    ActivationCodeGenerator,
)
from src.shared.utils.auth.password_manager import PasswordManager
from src.shared.utils.notifications.notificator import Notificator


class NameValidator:
    min_length = settings.users_name_min_length
    max_length = settings.users_name_max_length
    forbidden_names = settings.users_forbidden_names

    @classmethod
    def validate(cls, name: str):
        """Validates the name and raises a UserInvalidName if any rule is violated"""
        if not isinstance(name, str):
            raise UserInvalidName("Name must be a string")

        # Rule: Check if name is alphanumeric
        if not name.isalnum():
            raise UserInvalidName("Name can only contain alphanumeric characters.")

        # Rule: Check contains letters
        if not any(c.isalpha() for c in name):
            raise UserInvalidName("Name must contain at least one letter.")

        # Rule: Check length (too short)
        if len(name) < cls.min_length:
            raise UserInvalidName(
                f"Name is too short. Must be at least {cls.min_length} characters long."
            )

        # Rule: Check length (too long)
        if len(name) > cls.max_length:
            raise UserInvalidName(
                f"Name is too long. Must be no more than {cls.max_length} characters long."
            )

        # Rule: Check for forbidden names
        if name.lower() in cls.forbidden_names:
            raise UserInvalidName(
                f"The name {name} is forbidden. Please choose a different name."
            )


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
    password_manager.assert_password_valid(
        new_password, user_inputs=[user.username, user.email]
    )
    new_password_hash = password_manager.hash_password(new_password)
    user.change_password_hash(new_password_hash)
