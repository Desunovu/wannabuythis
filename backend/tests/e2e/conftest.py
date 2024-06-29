import pytest
from fastapi.testclient import TestClient

from src.common.dependencies.token_manager import JWTManager
from src.integration.entrypoints.fastapi_app import create_app


def add_authorization_header_to_client(client, user):
    token = JWTManager.generate_token(username=user.username)
    client.headers = {"Authorization": f"Bearer {token}"}


def add_user_to_db(client, user):
    with client.app.state.messagebus.uow as uow:
        uow.user_repository.add(user)
        uow.commit()


def add_user_and_role_to_db(client, user, role):
    with client.app.state.messagebus.uow as uow:
        uow.user_repository.add(user)
        uow.role_repository.add(role)
        uow.commit()


@pytest.fixture
def fastapi_app():
    return create_app()


@pytest.fixture
def fastapi_app_with_test_database(fastapi_app, sqlite_session_factory):
    fastapi_app.state.messagebus.uow.session_factory = sqlite_session_factory
    return fastapi_app


@pytest.fixture
def client(fastapi_app_with_test_database):
    return TestClient(fastapi_app_with_test_database)


@pytest.fixture
def admin_client(client, admin_user):
    """Test clent with signed in admin."""

    add_user_to_db(client, admin_user)
    add_authorization_header_to_client(client, admin_user)

    return client


@pytest.fixture
def admin_client_contains_deactivated_user(admin_client, deactivated_user):
    """Test clent with signed in admin. Contains deactivated user in db"""

    add_user_to_db(admin_client, deactivated_user)

    return admin_client


@pytest.fixture
def admin_client_contains_activated_user(admin_client, activated_user):
    """Test clent with signed in admin. Contains activated user in db"""

    add_user_to_db(admin_client, activated_user)

    return admin_client


@pytest.fixture
def admin_client_contains_user_and_default_role(admin_client, user, roles_default_role):
    """Test clent with signed in admin. Contains user and default role in db"""

    add_user_and_role_to_db(admin_client, user, roles_default_role)

    return admin_client


@pytest.fixture
def admin_client_contains_user_with_default_role(admin_client, user_with_default_role):
    """Test clent with signed in admin. Contains user with default role in db"""

    add_user_to_db(admin_client, user_with_default_role)

    return admin_client


@pytest.fixture
def client_with_deactivated_user(client, deactivated_user):
    """Test client. Contains deactivated user in db"""

    add_user_to_db(client, deactivated_user)

    return client


@pytest.fixture
def client_with_user(client, user):
    """Test client. Contains user in db"""

    add_user_to_db(client, user)

    return client


@pytest.fixture
def user_client(client_with_user, user):
    """Test clent with signed in user."""

    add_authorization_header_to_client(client_with_user, user)

    return client_with_user
