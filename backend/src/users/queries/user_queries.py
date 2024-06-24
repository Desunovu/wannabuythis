from sqlalchemy.orm import Session

from src.common.service.exceptions import UserNotFound
from src.users.domain.model import User


def get_user_by_username(session: Session, username: str) -> User:
    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise UserNotFound(username)
    return user
