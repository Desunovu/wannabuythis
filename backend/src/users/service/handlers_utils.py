from src.common.service.exceptions import UserNotFound
from src.common.service.uow import UnitOfWork


def check_user_exists(username: str, uow: UnitOfWork) -> bool:
    try:
        _user = uow.user_repository.get(username)
        return True
    except UserNotFound:
        return False
