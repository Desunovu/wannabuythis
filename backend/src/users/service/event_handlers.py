from src.common.adapters.activation_code_storage import ActivationCodeStorage
from src.common.utils.activation_code_generator import ActivationCodeGenerator
from src.common.utils.notificator import Notificator
from src.common.domain.events import DomainEvent
from src.common.service.uow import UnitOfWork
from src.users.domain.events import (
    EmailChanged,
    PasswordChanged,
    UserActivated,
    UserCreated,
    UserDeactivated,
)
from src.users.service.handlers_utils import send_new_activation_code


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
