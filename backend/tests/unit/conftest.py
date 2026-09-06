import pytest

from src.shared.application.mediator import Mediator
from src.shared.application.uow import UnitOfWork
from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.activation_codes.activation_code_generator import (
    ActivationCodeGenerator,
)
from tests.di.container import create_unit_test_container


# ---------------------------------------------------------------------------
# Dishka unit-test container fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def unit_test_container():
    return create_unit_test_container()


@pytest.fixture
def unit_test_request_container(unit_test_container):
    with unit_test_container() as request_container:
        yield request_container


@pytest.fixture
def messagebus(unit_test_request_container) -> Mediator:
    return unit_test_request_container.get(Mediator)


@pytest.fixture
def uow(unit_test_request_container) -> UnitOfWork:
    return unit_test_request_container.get(UnitOfWork)


@pytest.fixture
def activation_code_generator(unit_test_container) -> ActivationCodeGenerator:
    return unit_test_container.get(ActivationCodeGenerator)


@pytest.fixture
def activation_code_storage(unit_test_container) -> ActivationCodeStorage:
    return unit_test_container.get(ActivationCodeStorage)