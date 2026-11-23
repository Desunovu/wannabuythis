from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from src.modules.wishlists.domain.model import Wishlist
from src.modules.wishlists.infrastructure.wishlist_repository import WishlistRepository
from src.shared.application.exceptions import WishlistNotFound


class SQLAlchemyWishlistRepository(WishlistRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _wishlists_query(self):
        """Wishlists with items eagerly loaded; lazy="raise" forbids lazy loads."""
        return self.session.query(Wishlist).options(
            selectinload(Wishlist.items)  # pyright: ignore[reportArgumentType]
        )

    def _get(self, uuid: UUID) -> Wishlist:
        wishlist = (
            self._wishlists_query().filter_by(uuid=uuid).with_for_update().first()
        )
        if not wishlist:
            raise WishlistNotFound(uuid)
        return wishlist

    def _list_all(self) -> list[Wishlist]:
        return self._wishlists_query().all()

    def _list_owned_by(self, username: str) -> list[Wishlist]:
        return self._wishlists_query().filter_by(owner_username=username).all()

    def _add(self, wishlist: Wishlist):
        self.session.add(wishlist)
