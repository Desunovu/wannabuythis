from src.common.dependencies.notificator import Notificator
from src.common.dependencies.token_manager import TokenManager
from src.common.domain.events import DomainEvent
from src.common.service.uow import UnitOfWork
from src.users.domain.events import (
    EmailChanged,
    PasswordChanged,
    UserActivated,
    UserCreated,
    UserDeactivated,
)
from src.users.service.handlers_utils import send_notification_with_activation_link


def handle_user_created(
    event: UserCreated,
    uow: UnitOfWork,
    notificator: Notificator,
    token_manager: TokenManager,
):
    with uow:
        user = uow.user_repository.get(event.username)
    send_notification_with_activation_link(
        notificator=notificator, token_manager=token_manager, user=user
    )


USER_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [handle_user_created],
    PasswordChanged: [],
    EmailChanged: [],
    UserActivated: [],
    UserDeactivated: [],
}
