from dishka import FromDishka

from src.modules.users.application.handler_utils import send_new_activation_code
from src.modules.users.domain.events import (
    EmailChanged,
    PasswordChanged,
    UserActivated,
    UserCreated,
    UserDeactivated,
)
from src.shared.application.uow import UnitOfWork
from src.shared.domain.events import DomainEvent
from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.notifications.notificator import Notificator
from src.shared.utils.verification_codes.verification_code_generator import (
    VerificationCodeGenerator,
)


def handle_user_created(
    event: UserCreated,
    uow: FromDishka[UnitOfWork],
    notificator: FromDishka[Notificator],
    verification_code_generator: FromDishka[VerificationCodeGenerator],
    activation_code_storage: FromDishka[ActivationCodeStorage],
):
    with uow:
        user = uow.user_repository.get(event.username)
    send_new_activation_code(
        user=user,
        verification_code_generator=verification_code_generator,
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
