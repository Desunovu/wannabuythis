from src import config
from src.common.service.exceptions import PasswordValidationError, UserNotFound
from src.common.service.uow import UnitOfWork
from src.users.domain.model import User


def check_user_exists(username: str, uow: UnitOfWork) -> bool:
    try:
        _user = uow.user_repository.get(username)
        return True
    except UserNotFound:
        return False


def send_notification_with_activation_link(notificator, token_manager, user):
    token_lifetime = config.get_activation_token_lifetime()
    activation_token = token_manager.generate_token(
        username=user.username, token_lifetime=token_lifetime
    )
    notificator.send_activation_link(recipient=user, activation_token=activation_token)


def change_user_password(user, new_password, password_hash_util):
    if not User.validate_password(new_password):
        raise PasswordValidationError
    new_password_hash = password_hash_util.hash_password(new_password)
    user.change_password_hash(new_password_hash)
