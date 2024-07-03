from typing import Type
from uuid import UUID

from sqlalchemy.orm import Session

from src.common.service.exceptions import WishlistNotFound
from src.wishlists.adapters.wishlist_repository import WishlistRepository
from src.wishlists.domain.model import Wishlist


class SQLAlchemyWishlistRepository(WishlistRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _get(self, uuid: UUID) -> Wishlist:
        wishlist = (
            self.session.query(Wishlist).filter_by(uuid=uuid).with_for_update().first()
        )
        if not wishlist:
            raise WishlistNotFound(uuid)
        return wishlist

    def _list_all(self) -> list[Type[Wishlist]]:
        return self.session.query(Wishlist).all()

    def _list_owned_by(self, username: str) -> list[Type[Wishlist]]:
        return self.session.query(Wishlist).filter_by(owner_username=username).all()

    def _add(self, user: Wishlist):
        self.session.add(user)
