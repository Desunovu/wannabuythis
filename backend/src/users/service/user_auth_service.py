import datetime

from src.common.adapters.dependencies import PasswordHasher, TokenManager
from src.common.service.exceptions import (
    UserNotFound,
    UserNotActive,
    PasswordVerificationError,
)
from src.common.service.uow import UnitOfWork


class UserAuthService:
    def __init__(
            self,
            password_manager: PasswordHasher,
        token_manager: TokenManager,
            uow: UnitOfWork,
    ):
        self.password_manager = password_manager
        self.token_manager = token_manager
        self.uow = uow

    def generate_auth_token(
            self, username: str, password: str, exp_time: None | datetime.timedelta = None
    ) -> str:
        with self.uow as uow:
            user = uow.user_repository.get(username)
        if not user:
            raise UserNotFound(username=username)
        if not user.is_active:
            raise UserNotActive(username=username)
        if not self.password_manager.verify_password(
                password=password, password_hash=user.password_hash
        ):
            raise PasswordVerificationError

        # TODO: add expiration time from config
        token = self.token_manager.generate_token(
            username=user.username, exp_time=exp_time
        )

        return token

    def get_username_from_token(self, token: str) -> str:
        username = self.token_manager.get_username_from_token(token)
        return username
