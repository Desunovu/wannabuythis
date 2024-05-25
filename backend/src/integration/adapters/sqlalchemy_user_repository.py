from sqlalchemy.orm import Session

from src.users.adapters.user_repository import AbstractUserRepository
from src.users.domain.user import User


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _get(self, username: str) -> User | None:
        return (
            self.session.query(User)
            .filter_by(username=username)
            .with_for_update()
            .first()
        )

    def _add(self, user: User):
        self.session.add(user)
