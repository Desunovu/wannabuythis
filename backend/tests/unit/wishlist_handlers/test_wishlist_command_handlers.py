import uuid

import pytest

from src.common.service.exceptions import (
    UserNotFound,
    WishlistNotFound,
    WishlistItemNotFound,
)
from src.wishlists.domain.commands import (
    CreateWishlist,
    ChangeWishlistName,
    AddWishlistItem,
    RemoveWishlistItem,
)


class TestCreateWishlist:
    def test_create_wishlist(self, messagebus, user, wishlist_name):
        messagebus.uow.user_repository.add(user)
        messagebus.handle(
            CreateWishlist(owner_username=user.username, name=wishlist_name)
        )
        assert len(messagebus.uow.wishlist_repository.list_all()) == 1

    def test_create_wishlist_with_invalid_user(self, messagebus, wishlist_name):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                CreateWishlist(owner_username="non-existing-user", name=wishlist_name)
            )


class TestChangeWishlistName:
    def test_change_wishlist_name(self, messagebus, wishlist, wishlist_new_name):
        messagebus.uow.wishlist_repository.add(wishlist)
        messagebus.handle(
            ChangeWishlistName(uuid=wishlist.uuid, new_name=wishlist_new_name)
        )
        assert wishlist.name == wishlist_new_name

    def test_change_wishlist_name_non_existing_wishlist(
        self, messagebus, wishlist_new_name
    ):
        with pytest.raises(WishlistNotFound):
            messagebus.handle(
                ChangeWishlistName(uuid=uuid.uuid4(), new_name=wishlist_new_name)
            )


class TestAddWishlistItem:
    def test_add_wishlist_item(self, messagebus, wishlist):
        messagebus.uow.wishlist_repository.add(wishlist)
        messagebus.handle(
            AddWishlistItem(
                wishlist_uuid=wishlist.uuid,
                name="Apple",
                quantity=3,
                measurement_unit="kg.",
                priority=1,
            )
        )
        assert len(wishlist.items) == 1

    def test_add_wishlist_item_non_existing_wishlist(self, messagebus):
        with pytest.raises(WishlistNotFound):
            messagebus.handle(
                AddWishlistItem(
                    wishlist_uuid=uuid.uuid4(),
                    name="Apple",
                    quantity=3,
                    measurement_unit="kg.",
                    priority=1,
                )
            )


class TestRemoveWishlistItem:
    def test_remove_wishlist_item(self, messagebus, populated_wishlist):
        messagebus.uow.wishlist_repository.add(populated_wishlist)
        item_to_remove = populated_wishlist.items[0]
        messagebus.handle(
            RemoveWishlistItem(
                wishlist_uuid=populated_wishlist.uuid, item_uuid=item_to_remove.uuid
            )
        )
        assert item_to_remove not in populated_wishlist.items

    def test_remove_wishlist_item_non_existing_wishlist(self, messagebus, apple_item):
        with pytest.raises(WishlistNotFound):
            messagebus.handle(
                RemoveWishlistItem(
                    wishlist_uuid=uuid.uuid4(), item_uuid=apple_item.uuid
                )
            )

    def test_remove_wishlist_item_non_existing_wishlist_item(
        self, populated_wishlist, messagebus
    ):
        messagebus.uow.wishlist_repository.add(populated_wishlist)
        with pytest.raises(WishlistItemNotFound):
            messagebus.handle(
                RemoveWishlistItem(
                    wishlist_uuid=populated_wishlist.uuid, item_uuid=uuid.uuid4()
                )
            )
