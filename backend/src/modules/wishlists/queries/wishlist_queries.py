from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Select, desc, select
from sqlalchemy.orm import Session, load_only, selectinload

from src.modules.wishlists.domain.model import Wishlist
from src.shared.application.exceptions import WishlistNotFound
from src.shared.domain.username import Username, normalize_username


def get_wishlist_by_uuid(session: Session, uuid: UUID) -> Wishlist:
    """Load a wishlist with its items."""

    wishlist = session.get(
        Wishlist,
        uuid,
        options=[selectinload(Wishlist.items)],  # pyright: ignore[reportArgumentType]
    )
    if wishlist is None:
        raise WishlistNotFound(uuid)
    return wishlist


def get_wishlist_owner_username(session: Session, uuid: UUID) -> Username:
    """Return the wishlist owner's username without loading items."""

    wishlist = session.get(
        Wishlist,
        uuid,
        options=[load_only(Wishlist.owner_username)],  # pyright: ignore[reportArgumentType]
    )
    if wishlist is None:
        raise WishlistNotFound(uuid)
    return wishlist.owner_username


def _owned_wishlists_query(username: str):
    """Base query for a user's wishlists: eager items, newest first."""

    return (
        select(Wishlist)
        .options(selectinload(Wishlist.items))  # pyright: ignore[reportArgumentType]
        .filter_by(owner_username=normalize_username(username))
        .order_by(desc("created_at"), "uuid")
    )


def _fetch(
    session: Session,
    query: Select[tuple[Wishlist]],
    *,
    limit: int,
    offset: int,
) -> Sequence[Wishlist]:
    """Apply pagination and execute the query."""
    return session.scalars(query.limit(limit).offset(offset)).all()


def get_all_wishlists_by_username(
    session: Session, username: str, *, limit: int, offset: int = 0
) -> Sequence[Wishlist]:
    """Get all unarchived wishlists of a user, both private and public.

    For the owner's own listing or an admin view only. Public endpoints must
    use get_public_wishlists_by_username.
    """

    query = _owned_wishlists_query(username).filter_by(is_archived=False)
    return _fetch(session, query, limit=limit, offset=offset)


def get_public_wishlists_by_username(
    session: Session, username: str, *, limit: int, offset: int = 0
) -> Sequence[Wishlist]:
    """Get unarchived public wishlists of a user."""

    query = _owned_wishlists_query(username).filter_by(
        is_archived=False, is_public=True
    )
    return _fetch(session, query, limit=limit, offset=offset)


def get_archived_wishlists_by_username(
    session: Session, username: str, *, limit: int, offset: int = 0
) -> Sequence[Wishlist]:
    """Get archived wishlists of a user; archived wishlists are never public."""

    query = _owned_wishlists_query(username).filter_by(is_archived=True)
    return _fetch(session, query, limit=limit, offset=offset)
