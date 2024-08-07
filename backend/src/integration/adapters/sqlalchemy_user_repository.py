from sqlalchemy.orm import Session

from src.common.service.exceptions import UserNotFound
from src.users.adapters.user_repository import UserRepository
from src.users.domain.model import User


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _get(self, username: str) -> User:
        user = (
            self.session.query(User)
            .filter_by(username=username)
            .with_for_update()
            .first()
        )
        if not user:
            raise UserNotFound(username=username)
        return user

    def _add(self, user: User):
        self.session.add(user)
