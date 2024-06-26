import pytest
from fastapi.testclient import TestClient

from src.common.dependencies.token_manager import JWTManager
from src.integration.entrypoints.fastapi_app import create_app


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

    with client.app.state.messagebus.uow as uow:
        uow.user_repository.add(admin_user)
        uow.commit()

    token = JWTManager.generate_token(username=admin_user.username)
    client.headers = {"Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def admin_client_contains_deactivated_user(admin_client, deactivated_user):
    """Test clent with signed in admin. Contains deactivated user in db"""

    with admin_client.app.state.messagebus.uow as uow:
        uow.user_repository.add(deactivated_user)
        uow.commit()

    return admin_client


@pytest.fixture
def admin_client_contains_activated_user(admin_client, activated_user):
    """Test clent with signed in admin. Contains activated user in db"""

    with admin_client.app.state.messagebus.uow as uow:
        uow.user_repository.add(activated_user)
        uow.commit()

    return admin_client


@pytest.fixture
def admin_client_contains_user_and_default_role(admin_client, user, roles_default_role):
    """Test clent with signed in admin. Contains user and default role in db"""

    with admin_client.app.state.messagebus.uow as uow:
        uow.user_repository.add(user)
        uow.role_repository.add(roles_default_role)
        uow.commit()

    return admin_client


@pytest.fixture
def admin_client_contains_user_with_default_role(admin_client, user_with_default_role):
    """Test clent with signed in admin. Contains user with default role in db"""

    with admin_client.app.state.messagebus.uow as uow:
        uow.user_repository.add(user_with_default_role)
        uow.commit()

    return admin_client
