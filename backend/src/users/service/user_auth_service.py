from src.common.adapters.dependencies import PasswordHasher, AuthTokenManager
from src.common.service.exceptions import (
    UserNotFound,
    UserNotActive,
    PasswordVerificationError,
)
from src.common.service.uow import UnitOfWork


def generate_token(
    username: str,
    password: str,
    password_manager: PasswordHasher,
    token_manager: AuthTokenManager,
    uow: UnitOfWork,
) -> str:
    with uow:
        user = uow.user_repository.get(username)
    if not user:
        raise UserNotFound
    if not user.is_active:
        raise UserNotActive
    if not password_manager.verify_password(
        password=password, password_hash=user.password_hash
    ):
        raise PasswordVerificationError

    token = token_manager.generate_token(user.email)

    return token
