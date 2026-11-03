import pytest

from src.shared.application.mediator import Mediator
from src.shared.application.uow import UnitOfWork
from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.verification_codes.verification_code_generator import (
    VerificationCodeGenerator,
)
from tests.di.container import create_unit_test_container


@pytest.fixture
def unit_test_container():
    container = create_unit_test_container()
    yield container
    container.close()


@pytest.fixture
def unit_test_request_container(unit_test_container):
    with unit_test_container() as request_container:
        yield request_container


@pytest.fixture
def mediator(unit_test_request_container) -> Mediator:
    return unit_test_request_container.get(Mediator)


@pytest.fixture
def uow(unit_test_request_container) -> UnitOfWork:
    return unit_test_request_container.get(UnitOfWork)


@pytest.fixture
def verification_code_generator(unit_test_container) -> VerificationCodeGenerator:
    return unit_test_container.get(VerificationCodeGenerator)


@pytest.fixture
def activation_code_storage(unit_test_container) -> ActivationCodeStorage:
    return unit_test_container.get(ActivationCodeStorage)
