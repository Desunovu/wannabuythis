import pytest

from src.common.service.exceptions import UserNotFound, WishlistNotFound, WishlistItemNotFound
from src.wishlists.domain.commands import CreateWishlist, ChangeWishlistName, AddWishlistItem, RemoveWishlistItem


class TestCreateWishlist:
    def test_create_wishlist(self, messagebus, user):
        messagebus.uow.user_repository.add(user)
        messagebus.handle(
            CreateWishlist(owner_username=user.username, name="testwishlist")
        )
        new_wishlist = messagebus.uow.wishlist_repository.list_owned_by(user.username)[
            0
        ]
        assert new_wishlist.name == "testwishlist"

    def test_create_wishlist_with_invalid_user(self, messagebus):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                CreateWishlist(owner_username="testuser", name="testwishlist")
            )


class TestChangeWishlistName:
    def test_change_wishlist_name(self, messagebus, wishlist):
        messagebus.uow.wishlist_repository.add(wishlist)
        messagebus.handle(ChangeWishlistName(uuid=wishlist.uuid, new_name="New Name"))
        assert wishlist.name == "New Name"

    def test_change_wishlist_name_non_existing_wishlist(self, messagebus):
        with pytest.raises(WishlistNotFound):
            messagebus.handle(
                ChangeWishlistName(uuid="non-existing-wishlist", new_name="New Name")
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
                    wishlist_uuid="non-existing-wishlist",
                    name="Apple",
                    quantity=3,
                    measurement_unit="kg.",
                    priority=1,
                )
            )


class TestRemoveWishlistItem:
    def test_remove_wishlist_item(self, messagebus, populated_wishlist, apple_item):
        messagebus.uow.wishlist_repository.add(populated_wishlist)
        messagebus.handle(
            RemoveWishlistItem(
                wishlist_uuid=populated_wishlist.uuid, item_uuid=apple_item.uuid
            )
        )

        assert apple_item not in populated_wishlist.items

    def test_remove_wishlist_item_non_existing_wishlist(self, messagebus, apple_item):
        with pytest.raises(WishlistNotFound):
            messagebus.handle(
                RemoveWishlistItem(
                    wishlist_uuid="non-existing-wishlist", item_uuid=apple_item.uuid
                )
            )

    def test_remove_wishlist_item_non_existing_wishlist_item(
        self, populated_wishlist, messagebus
    ):
        messagebus.uow.wishlist_repository.add(populated_wishlist)
        with pytest.raises(WishlistItemNotFound):
            messagebus.handle(
                RemoveWishlistItem(
                    wishlist_uuid=populated_wishlist.uuid,
                    item_uuid="non-existing-wishlist-item",
                )
            )
