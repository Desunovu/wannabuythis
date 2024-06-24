from sqlalchemy.orm import Session

from src.common.service.exceptions import RoleNotFound
from src.roles.adapters.role_repository import RoleRepository
from src.roles.domain.model import Role


class SQLAlchemyRoleRepository(RoleRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _get(self, name) -> Role:
        role = self.session.query(Role).filter_by(name=name).with_for_update().first()
        if not role:
            raise RoleNotFound
        return role

    def _add(self, role: Role):
        self.session.add(role)
