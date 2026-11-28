from collections.abc import Generator
from contextlib import contextmanager

from dishka import Container
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.config import settings
from src.modules.users.domain.model import User
from src.modules.wishlists.domain.model import Wishlist
from src.shared.application.uow import UnitOfWork
from src.shared.utils.auth.token_manager import TokenManager


def _get_container(client: TestClient) -> Container:
    app = client.app
    assert isinstance(app, FastAPI)
    return app.state.dishka_container


@contextmanager
def app_uow(client: TestClient) -> Generator[UnitOfWork]:
    """Open a unit of work bound to the application's request container."""
    container = _get_container(client)
    with container() as request_container:
        uow = request_container.get(UnitOfWork)
        with uow:
            yield uow


def add_user_to_db(client: TestClient, user: User) -> None:
    with app_uow(client) as uow:
        uow.user_repository.add(user)
        uow.commit()


def add_wishlist_to_db(client: TestClient, wishlist: Wishlist) -> None:
    with app_uow(client) as uow:
        uow.wishlist_repository.add(wishlist)
        uow.commit()


def add_authorization_header_to_client(client: TestClient, user: User) -> None:
    container = _get_container(client)
    token_manager = container.get(TokenManager)
    token = token_manager.create_access_token(
        username=user.username, token_lifetime=settings.access_token_lifetime
    )
    client.headers = {"Authorization": f"Bearer {token}"}
