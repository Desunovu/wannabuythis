from uuid import UUID

from sqlalchemy.orm import Session

from src.common.service.exceptions import WishlistNotFound
from src.wishlists.domain.model import Wishlist


def get_wishlist_by_uuid(session: Session, uuid: UUID) -> Wishlist:
    """SQLAlchemy query to get a wishlist by its UUID."""

    wishlist = session.query(Wishlist).filter_by(uuid=uuid).first()
    if not wishlist:
        raise WishlistNotFound(uuid=uuid)
    return wishlist


def get_wishlists_owned_by(session: Session, username: str) -> list[Wishlist]:
    """SQLAlchemy query to get all wishlists owned by a user."""

    return session.query(Wishlist).filter_by(owner_username=username).all()


def get_archived_wishlists_owned_by(session: Session, username: str) -> list[Wishlist]:
    """SQLAlchemy query to get all archived wishlists owned by a user."""

    return (
        session.query(Wishlist)
        .filter_by(owner_username=username, is_archived=True)
        .all()
    )
