import pytest

from src.domain.user.commands import CreateUser, ChangePassword
from src.domain.wishlist.commands import (
    CreateWishlist,
    ChangeWishlistName,
    AddWishlistItem,
    RemoveWishlistItem,
)
from src.service_layer.handlers.exceptions import (
    UserNotFound,
    UserExists,
    InvalidPassword,
    InvalidOldPassword,
    WishlistNotFound,
    WishlistItemNotFound,
)


class TestCreateUser:
    def test_create_new_user(self, messagebus, valid_password):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_password)
        )

        assert messagebus.uow.user_repository.get("testuser") is not None

    def test_create_existing_user(self, messagebus, valid_password):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_password)
        )

        with pytest.raises(UserExists):
            messagebus.handle(
                CreateUser("testuser", "testemail@example.com", valid_password)
            )


class TestChangePassword:
    def test_change_password_by_admin(
        self, messagebus, valid_password, valid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        user = messagebus.uow.user_repository.get("testuser")
        old_password_hash = user.password_hash
        messagebus.handle(
            ChangePassword("testuser", valid_password, called_by_admin=True)
        )

        assert user.password_hash != old_password_hash

    def test_change_password_by_user(
        self, messagebus, valid_password, valid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        user = messagebus.uow.user_repository.get("testuser")
        old_password_hash = user.password_hash
        messagebus.handle(
            ChangePassword("testuser", valid_password, valid_old_password)
        )

        assert user.password_hash != old_password_hash

    def test_change_password_non_existing_user(self, messagebus, valid_password):
        with pytest.raises(UserNotFound):
            messagebus.handle(
                ChangePassword("testuser", valid_password, valid_password)
            )

    def test_change_password_invalid_old_password(
        self, messagebus, valid_password, valid_old_password, invalid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        with pytest.raises(InvalidOldPassword):
            messagebus.handle(
                ChangePassword("testuser", valid_password, invalid_old_password)
            )

    def test_change_password_invalid_password(
        self, messagebus, invalid_password, valid_old_password
    ):
        messagebus.handle(
            CreateUser("testuser", "testemail@example.com", valid_old_password)
        )
        with pytest.raises(InvalidPassword):
            messagebus.handle(
                ChangePassword("testuser", invalid_password, valid_old_password)
            )


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
