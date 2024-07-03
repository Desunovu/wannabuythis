import uuid

import pytest

from src.common.service.exceptions import UserNotFound, WishlistNotFound
from src.integration.adapters.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.integration.adapters.sqlalchemy_wishlist_repository import (
    SQLAlchemyWishlistRepository,
)


class TestSQLAlchemyUserRepository:
    def test_get_user(self, sqlite_session, user):
        sqlite_session.add(user)
        sqlite_session.commit()
        repository = SQLAlchemyUserRepository(sqlite_session)
        assert repository.get(user.username) is not None

    def test_get_non_existing_user(self, sqlite_session):
        repository = SQLAlchemyUserRepository(sqlite_session)
        with pytest.raises(UserNotFound):
            user = repository.get("non-existing-user")

    def test_add_user(self, sqlite_session, user):
        repository = SQLAlchemyUserRepository(sqlite_session)
        repository.add(user)
        assert repository.get(user.username) is not None


class TestSQLAlchemyWishlistRepository:
    def test_get_wishlist(self, sqlite_session, wishlist):
        sqlite_session.add(wishlist)
        sqlite_session.commit()
        repository = SQLAlchemyWishlistRepository(sqlite_session)
        assert repository.get(wishlist.uuid) is not None

    def test_get_non_existing_wishlist(self, sqlite_session):
        repository = SQLAlchemyWishlistRepository(sqlite_session)
        with pytest.raises(WishlistNotFound):
            wishlist = repository.get(uuid.uuid4())

    def test_list_all_wishlists(self, sqlite_session, wishlist, populated_wishlist):
        sqlite_session.add_all([wishlist, populated_wishlist])
        sqlite_session.commit()
        repository = SQLAlchemyWishlistRepository(sqlite_session)
        assert repository.list_all() == [wishlist, populated_wishlist]

    def test_list_wishlists_owned_by(
        self, sqlite_session, user, wishlist, populated_wishlist
    ):
        sqlite_session.add_all([user, wishlist, populated_wishlist])
        sqlite_session.commit()
        repository = SQLAlchemyWishlistRepository(sqlite_session)
        assert repository.list_owned_by(user.username) == [wishlist, populated_wishlist]

    def test_add_wishlist(self, sqlite_session, wishlist):
        repository = SQLAlchemyWishlistRepository(sqlite_session)
        repository.add(wishlist)
        assert repository.get(wishlist.uuid) is not None
