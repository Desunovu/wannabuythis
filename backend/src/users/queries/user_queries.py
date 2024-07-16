from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common.service.exceptions import UserNotFound
from src.users.domain.model import User


def get_all_users(session: Session) -> list[User]:
    return session.scalars(select(User)).all()


def get_user_by_username(session: Session, username: str) -> User:
    user = session.get(User, username)
    if user is None:
        raise UserNotFound(username)
    return user
