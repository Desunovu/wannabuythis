import datetime
import uuid
from collections.abc import Iterator
from contextlib import contextmanager

import pytest
from sqlalchemy import Connection, Engine, event
from sqlalchemy.exc import InvalidRequestError

from src.modules.users.domain.model import User
from src.modules.wishlists.domain.model import (
    MeasurementUnit,
    Priority,
    Wishlist,
    WishlistItem,
)
from src.modules.wishlists.queries import wishlist_queries
from src.shared.application.exceptions import WishlistNotFound
from src.shared.application.uow import UnitOfWork
from src.shared.domain.username import Username


def make_wishlist(
    owner_username: Username, name: str, *, items_count: int = 2
) -> Wishlist:
    wishlist_uuid = uuid.uuid4()
    return Wishlist(
        uuid=wishlist_uuid,
        owner_username=owner_username,
        name=name,
        items=[
            WishlistItem(
                uuid=uuid.uuid4(),
                wishlist_uuid=wishlist_uuid,
                name=f"item {index}",
                quantity=1,
                measurement_unit=MeasurementUnit.PIECE,
                priority=Priority.LOW,
            )
            for index in range(items_count)
        ],
        created_at=datetime.datetime.now(datetime.UTC),
    )


def seed_owned_wishlists(
    uow: UnitOfWork, user: User, *, count: int = 1
) -> list[Wishlist]:
    wishlists = [
        make_wishlist(user.username, f"wishlist {index}") for index in range(count)
    ]
    with uow:
        uow.user_repository.add(user)
        for wishlist in wishlists:
            uow.wishlist_repository.add(wishlist)
        uow.commit()
    return wishlists


@contextmanager
def capture_selects(bind: Engine | Connection) -> Iterator[list[str]]:
    statements: list[str] = []

    def record_select(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(bind, "before_cursor_execute", record_select)
    try:
        yield statements
    finally:
        event.remove(bind, "before_cursor_execute", record_select)


class TestWishlistQueries:
    def test_list_query_loads_items_with_two_selects(
        self, sqlalchemy_uow, db_session, user
    ):
        seed_owned_wishlists(sqlalchemy_uow, user, count=3)

        with capture_selects(db_session.get_bind()) as select_statements:
            wishlists = wishlist_queries.get_all_wishlists_by_username(
                db_session, user.username, limit=10
            )
            assert all(len(wishlist.items) == 2 for wishlist in wishlists)

        assert len(wishlists) == 3
        # One SELECT for wishlists plus one selectinload for their items.
        assert len(select_statements) == 2

    def test_items_are_never_loaded_lazily(self, sqlalchemy_uow, db_session, user):
        wishlist = seed_owned_wishlists(sqlalchemy_uow, user)[0]

        loaded = db_session.get(Wishlist, wishlist.uuid)

        assert loaded is not None
        with pytest.raises(InvalidRequestError):
            _ = loaded.items


class TestWishlistOwnerQuery:
    def test_returns_owner_username(self, sqlalchemy_uow, db_session, user):
        wishlist = seed_owned_wishlists(sqlalchemy_uow, user)[0]

        assert (
            wishlist_queries.get_wishlist_owner_username(db_session, wishlist.uuid)
            == user.username
        )

    def test_missing_wishlist_raises(self, db_session):
        with pytest.raises(WishlistNotFound):
            wishlist_queries.get_wishlist_owner_username(db_session, uuid.uuid4())
