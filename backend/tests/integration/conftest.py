import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import clear_mappers

from src.config import settings
from src.infrastructure.database.sqlalchemy.orm import (
    start_sqlalchemy_mappers,
)
from src.infrastructure.entrypoints.fastapi.app import create_app
from src.shared.application.uow import UnitOfWork
from src.shared.utils.auth.token_manager import TokenManager
from tests.di.container import create_integration_test_container


def add_authorization_header_to_client(client: TestClient, user) -> None:
    container = client.app.state.dishka_container
    token_manager = container.get(TokenManager)
    token = token_manager.generate_token(username=user.username)
    client.headers = {"Authorization": f"Bearer {token}"}


def add_user_to_db(client: TestClient, user) -> None:
    container = client.app.state.dishka_container
    with container() as request_container:
        uow = request_container.get(UnitOfWork)
        with uow:
            uow.user_repository.add(user)
            uow.commit()


def add_wishlist_to_db(client: TestClient, wishlist) -> None:
    container = client.app.state.dishka_container
    with container() as request_container:
        uow = request_container.get(UnitOfWork)
        with uow:
            uow.wishlist_repository.add(wishlist)
            uow.commit()


@pytest.fixture
def integration_test_container():
    start_sqlalchemy_mappers()
    container = create_integration_test_container()
    with container() as request_container:
        yield request_container
    container.close()
    clear_mappers()


@pytest.fixture
def sqlalchemy_uow(integration_test_container) -> UnitOfWork:
    return integration_test_container.get(UnitOfWork)


@pytest.fixture
def prepare_mappers():
    start_sqlalchemy_mappers()
    yield
    clear_mappers()


@pytest.fixture
def fastapi_app_with_test_database(monkeypatch):
    # TODO: remove monkeypatch
    monkeypatch.setattr(settings, "env", "testing")
    test_container = create_integration_test_container()
    app = create_app(container=test_container)

    yield app

    test_container.close()


@pytest.fixture
def client(fastapi_app_with_test_database) -> TestClient:
    with TestClient(fastapi_app_with_test_database) as test_client:
        yield test_client


@pytest.fixture
def user_client(client: TestClient, user) -> TestClient:
    """Test client with a signed-in user."""
    add_user_to_db(client, user)
    add_authorization_header_to_client(client, user)
    return client


@pytest.fixture
def admin_client(client: TestClient, admin_user) -> TestClient:
    """Test client with a signed-in admin."""
    add_user_to_db(client, admin_user)
    add_authorization_header_to_client(client, admin_user)
    return client


@pytest.fixture
def client_with_user(client: TestClient, user) -> TestClient:
    """Test client containing a user in the database."""
    add_user_to_db(client, user)
    return client


@pytest.fixture
def client_with_populated_wishlist(
    client_with_user: TestClient, populated_wishlist
) -> TestClient:
    """Test client containing a user and their populated wishlist in the database."""
    add_wishlist_to_db(client_with_user, populated_wishlist)
    return client_with_user


@pytest.fixture
def user_with_populated_wishlist_client(
    user_client: TestClient, populated_wishlist
) -> TestClient:
    """Test client with a signed-in user containing their populated wishlist in the database."""
    add_wishlist_to_db(user_client, populated_wishlist)
    return user_client


@pytest.fixture
def user_with_archived_wishlist_client(
    user_client: TestClient, archived_wishlist
) -> TestClient:
    """Test client with a signed-in user containing their archived wishlist in the database."""
    add_wishlist_to_db(user_client, archived_wishlist)
    return user_client


@pytest.fixture
def admin_client_contains_deactivated_user(
    admin_client: TestClient, deactivated_user
) -> TestClient:
    """Test client with a signed-in admin containing a deactivated user in the database."""
    add_user_to_db(admin_client, deactivated_user)
    return admin_client


@pytest.fixture
def admin_client_contains_activated_user(
    admin_client: TestClient, activated_user
) -> TestClient:
    """Test client with a signed-in admin containing an activated user in the database."""
    add_user_to_db(admin_client, activated_user)
    return admin_client


@pytest.fixture
def client_with_deactivated_user(client: TestClient, deactivated_user) -> TestClient:
    """Test client containing a deactivated user in the database."""
    add_user_to_db(client, deactivated_user)
    return client


@pytest.fixture
def client_with_deactivated_user_token(
    client_with_deactivated_user, deactivated_user
) -> TestClient:
    """Test client bearing a token issued to a deactivated user."""
    add_authorization_header_to_client(client_with_deactivated_user, deactivated_user)
    return client_with_deactivated_user
