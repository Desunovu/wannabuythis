from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common.service.exceptions import WishlistNotFound
from src.wishlists.domain.model import Wishlist


def get_wishlist_by_uuid(session: Session, uuid: UUID) -> Wishlist:
    """SQLAlchemy query to get a wishlist by its UUID."""

    wishlist = session.get(Wishlist, uuid)
    if wishlist is None:
        raise WishlistNotFound(uuid=uuid)
    return wishlist


def get_wishlists_owned_by(session: Session, username: str) -> list[Wishlist]:
    """SQLAlchemy query to get all unarchived wishlists owned by a user."""

    wishlists = session.scalars(
        select(Wishlist)
        .filter_by(owner_username=username, is_archived=False)
        .order_by(Wishlist.created_at.desc())
    ).all()
    return wishlists


def get_archived_wishlists_owned_by(session: Session, username: str) -> list[Wishlist]:
    """SQLAlchemy query to get all archived wishlists owned by a user."""

    wishlists = session.scalars(
        select(Wishlist).filter_by(owner_username=username, is_archived=True)
    ).all()
    return wishlists
