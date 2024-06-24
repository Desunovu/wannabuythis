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


def handle_user_created(event: UserCreated, notificator: Notificator):
    notificator.send_notification(event.username, "Welcome", "Welcome to our site")


USER_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [handle_user_created],
    PasswordChanged: [],
    EmailChanged: [],
    UserActivated: [],
    UserDeactivated: [],
    RoleAddedToUser: [],
    RoleRemovedFromUser: [],
}
