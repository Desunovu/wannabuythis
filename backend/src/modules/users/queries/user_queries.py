from sqlalchemy import select
from sqlalchemy.orm import Session, load_only

from src.core.service.exceptions import UserNotFound
from src.modules.users.domain.model import User


def get_all_users(session: Session) -> list[User]:
    stmt = select(User).options(load_only(User.username))
    users = session.scalars(stmt).all()
    return users


def get_user_by_username(session: Session, username: str) -> User:
    user = session.get(
        User,
        username,
        options=[load_only(User.username)],
    )
    if user is None:
        raise UserNotFound(username)
    return user
