from src.common.dependencies.notificator import Notificator
from src.common.dependencies.token_manager import TokenManager
from src.common.domain.events import DomainEvent
from src.common.service.uow import UnitOfWork
from src.users.domain.events import (
    UserCreated,
    PasswordChanged,
    EmailChanged,
    UserActivated,
    UserDeactivated,
)


def handle_user_created(
    event: UserCreated,
    uow: UnitOfWork,
    notificator: Notificator,
    token_manager: TokenManager,
):
    user = uow.user_repository.get(event.username)
    # TODO set activation token expiration time from config
    activation_token = token_manager.generate_token(
        username=event.username, exp_time=None
    )
    notificator.send_activation_link(recipient=user, activation_token=activation_token)


USER_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [handle_user_created],
    PasswordChanged: [],
    EmailChanged: [],
    UserActivated: [],
    UserDeactivated: [],
}
