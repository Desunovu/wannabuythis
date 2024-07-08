from sqlalchemy.orm import Session

from src.common.service.exceptions import UserNotFound
from src.users.domain.model import User


def get_user_by_username(session: Session, username: str) -> User:
    user = session.get(User, username)
    if user is None:
        raise UserNotFound(username)
    return user
