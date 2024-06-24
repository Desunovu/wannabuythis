from src.common.service.exceptions import UserNotFound, RoleNotFound
from src.common.service.uow import UnitOfWork


def check_role_exists(role_name: str, uow: UnitOfWork) -> bool:
    try:
        _role = uow.role_repository.get(role_name)
        return True
    except RoleNotFound:
        return False
