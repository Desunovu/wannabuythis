from collections.abc import Generator
from contextlib import contextmanager

from fastapi.testclient import TestClient

from src.config import settings
from src.shared.application.uow import UnitOfWork
from src.shared.utils.auth.token_manager import TokenManager


@contextmanager
def app_uow(client: TestClient) -> Generator[UnitOfWork]:
    """Open a unit of work bound to the application's request container."""
    container = client.app.state.dishka_container
    with container() as request_container:
        uow = request_container.get(UnitOfWork)
        with uow:
            yield uow


def add_user_to_db(client: TestClient, user) -> None:
    with app_uow(client) as uow:
        uow.user_repository.add(user)
        uow.commit()


def add_wishlist_to_db(client: TestClient, wishlist) -> None:
    with app_uow(client) as uow:
        uow.wishlist_repository.add(wishlist)
        uow.commit()


def add_authorization_header_to_client(client: TestClient, user) -> None:
    container = client.app.state.dishka_container
    token_manager = container.get(TokenManager)
    token = token_manager.create_access_token(
        username=user.username, token_lifetime=settings.access_token_lifetime
    )
    client.headers = {"Authorization": f"Bearer {token}"}
