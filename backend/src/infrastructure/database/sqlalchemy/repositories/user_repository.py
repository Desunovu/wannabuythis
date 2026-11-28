from sqlalchemy.orm import Session

from src.modules.users.domain.model import User
from src.modules.users.infrastructure.user_repository import UserRepository
from src.shared.application.exceptions import UserNotFound


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _get_by_username(self, username: str, *, for_update: bool = True) -> User:
        query = self.session.query(User).filter_by(username=username)
        if for_update:
            query = query.with_for_update()
        user = query.first()
        if not user:
            raise UserNotFound(username=username)
        return user

    def _get_by_email(self, email: str) -> User:
        user = self.session.query(User).filter_by(email=email).first()
        if not user:
            raise UserNotFound(username=email)
        return user

    def _add(self, user: User):
        self.session.add(user)
