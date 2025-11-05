from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.activation_codes.activation_code_generator import (
    ActivationCodeGenerator,
)
from src.shared.utils.notifications.notificator import Notificator
from src.shared.domain.events import DomainEvent
from src.shared.application.uow import UnitOfWork
from src.modules.users.domain.events import (
    EmailChanged,
    PasswordChanged,
    UserActivated,
    UserCreated,
    UserDeactivated,
)
from src.modules.users.application.handler_utils import send_new_activation_code


def handle_user_created(
    event: UserCreated,
    uow: UnitOfWork,
    notificator: Notificator,
    activation_code_generator: ActivationCodeGenerator,
    activation_code_storage: ActivationCodeStorage,
):
    with uow:
        user = uow.user_repository.get(event.username)
    send_new_activation_code(
        user=user,
        activation_code_generator=activation_code_generator,
        activation_code_storage=activation_code_storage,
        notificator=notificator,
    )


USER_EVENT_HANDLERS: dict[type[DomainEvent], list[callable]] = {
    UserCreated: [handle_user_created],
    PasswordChanged: [],
    EmailChanged: [],
    UserActivated: [],
    UserDeactivated: [],
}
