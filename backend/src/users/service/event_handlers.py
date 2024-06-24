from src.common.adapters.dependencies import Notificator, TokenManager
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


def handle_user_created(
    event: UserCreated,
    notificator: Notificator,
    token_manager: TokenManager,
):
    # TODO set activation token expiration time from config
    activation_token = token_manager.generate_token(
        username=event.username, exp_time=None
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
