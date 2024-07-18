import pytest
from fastapi.testclient import TestClient
from src.common.utils.token_manager import JWTManager
from src.integration.entrypoints.fastapi_app import create_app


def add_authorization_header_to_client(client: TestClient, user) -> None:
    token = JWTManager.generate_token(username=user.username)
    client.headers = {"Authorization": f"Bearer {token}"}


def add_user_to_db(client: TestClient, user) -> None:
    with client.app.state.messagebus.uow as uow:
        uow.user_repository.add(user)
        uow.commit()


def add_wishlist_to_db(client: TestClient, wishlist) -> None:
    with client.app.state.messagebus.uow as uow:
        uow.wishlist_repository.add(wishlist)
        uow.commit()


@pytest.fixture(scope="session")
def fastapi_app():
    return create_app()


@pytest.fixture
def fastapi_app_with_test_database(fastapi_app, sqlite_session_factory):
    fastapi_app.state.messagebus.uow.session_factory = sqlite_session_factory
    return fastapi_app


@pytest.fixture
def client(fastapi_app_with_test_database) -> TestClient:
    return TestClient(fastapi_app_with_test_database)


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
