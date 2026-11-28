from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.users.domain.model import User
from src.shared.application.exceptions import UserNotFound
from src.shared.domain.username import normalize_username


def get_all_users(session: Session) -> Sequence[User]:
    return session.scalars(select(User)).all()


def get_user_by_username(session: Session, username: str) -> User:
    user = session.get(User, normalize_username(username))
    if user is None:
        raise UserNotFound(username)
    return user
