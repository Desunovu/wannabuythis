from src import config
from src.common.service.exceptions import UserNotFound
from src.common.service.uow import UnitOfWork


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
