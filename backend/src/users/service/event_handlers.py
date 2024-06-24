from src.common.adapters.dependencies import Notificator
from src.common.domain.events import DomainEvent
from src.users.domain.events import (
    UserCreated,
    PasswordChanged,
    EmailChanged,
    UserActivated,
    UserDeactivated,
    RoleAddedToUser,
    RoleRemovedFromUser,
)
from src.users.service.user_auth_service import UserAuthService


def handle_user_created(
        event: UserCreated,
        user_auth_service: UserAuthService,
        notificator: Notificator,
):
    activation_token = user_auth_service.generate_activation_token(
        username=event.username
    )
    notificator.send_activation_link(
        recipient=event.email, activation_token=activation_token
    )


USER_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [handle_user_created],
    PasswordChanged: [],
    EmailChanged: [],
    UserActivated: [],
    UserDeactivated: [],
    RoleAddedToUser: [],
    RoleRemovedFromUser: [],
}
