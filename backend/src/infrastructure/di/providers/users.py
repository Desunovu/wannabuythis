from dishka import Provider, Scope, provide

from src.modules.users.application.refresh_token_service import RefreshTokenService


class UsersProvider(Provider):
    @provide(scope=Scope.APP)
    def get_refresh_token_service(self) -> RefreshTokenService:
        return RefreshTokenService()
