import uuid

from src.integration.adapters.sqlalchemy_orm import start_mappers
from src.users.domain.user import User
from src.wishlists.domain.wishlist import Wishlist
from src.wishlists.domain.wishlist_item import WishlistItem, Priority, MeasurementUnit


def test_start_mappers(sqlite_session_factory):
    start_mappers()
    session = sqlite_session_factory()

    # Test mapping of User
    assert session.query(User).first() is None
    user = User(
        username="testuser", email="testemail@example.com", password_hash="password"
    )
    session.add(user)
    session.commit()
    assert session.query(User).first().username == "testuser"

    # Test mapping of Wishlist
    assert session.query(Wishlist).first() is None
    wishlist = Wishlist(
        uuid=uuid.uuid4(),
        owner_username="testuser",
        name="testwishlist",
        items=[],
    )
    session.add(wishlist)
    session.commit()
    assert session.query(Wishlist).first().name == "testwishlist"

    # Test mapping of WishlistItem and its value-objects
    assert session.query(WishlistItem).first() is None
    wishlist_item = WishlistItem(
        uuid=uuid.uuid4(),
        wishlist_uuid=uuid.uuid4(),
        name="testwishlistitem",
        quantity=1,
        measurement_unit=MeasurementUnit(name="kg."),
        priority=Priority(value=1),
    )
    session.add(wishlist_item)
    session.commit()
    wishlist_item_from_db: WishlistItem = session.query(WishlistItem).first()
    assert wishlist_item_from_db.name == "testwishlistitem"
    assert wishlist_item_from_db.measurement_unit.name == "kg."
    assert wishlist_item_from_db.priority.value == 1
