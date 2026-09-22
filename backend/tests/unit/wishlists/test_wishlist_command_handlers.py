import uuid

import pytest

from src.modules.wishlists.domain.commands import (
    AddWishlistItem,
    ArchiveWishlist,
    ChangeWishlistName,
    ChangeWishlistVisibility,
    CreateWishlist,
    MarkWishlistItemAsNotPurchased,
    MarkWishlistItemAsPurchased,
    RemoveWishlistItem,
    UnarchiveWishlist,
)
from src.modules.wishlists.domain.model import MeasurementUnit, Priority
from src.shared.application.exceptions import (
    UserNotFound,
    WishlistAlreadyArchived,
    WishlistItemAlreadyPurchased,
    WishlistItemNotFound,
    WishlistItemNotPurchased,
    WishlistNotArchived,
    WishlistNotFound,
)


class TestCreateWishlist:
    def test_create_private_wishlist(self, mediator, uow, user, wishlist_name):
        uow.user_repository.add(user)
        mediator.handle(
            CreateWishlist(
                owner_username=user.username, name=wishlist_name, is_public=False
            )
        )
        assert len(uow.wishlist_repository.list_all()) == 1
        assert uow.wishlist_repository.list_all()[0].is_public is False

    def test_create_public_wishlist(self, mediator, uow, user, wishlist_name):
        uow.user_repository.add(user)
        mediator.handle(
            CreateWishlist(
                owner_username=user.username, name=wishlist_name, is_public=True
            )
        )
        assert uow.wishlist_repository.list_all()[0].is_public is True

    def test_create_wishlist_with_invalid_user(self, mediator, wishlist_name):
        with pytest.raises(UserNotFound):
            mediator.handle(
                CreateWishlist(
                    owner_username="non-existing-user",
                    name=wishlist_name,
                    is_public=False,
                )
            )


class TestChangeWishlistName:
    def test_change_wishlist_name(self, mediator, uow, wishlist, wishlist_new_name):
        uow.wishlist_repository.add(wishlist)
        mediator.handle(
            ChangeWishlistName(uuid=wishlist.uuid, new_name=wishlist_new_name)
        )
        assert wishlist.name == wishlist_new_name

    def test_change_wishlist_name_non_existing_wishlist(
        self, mediator, wishlist_new_name
    ):
        with pytest.raises(WishlistNotFound):
            mediator.handle(
                ChangeWishlistName(uuid=uuid.uuid4(), new_name=wishlist_new_name)
            )


class TestAddWishlistItem:
    def test_add_wishlist_item(self, mediator, uow, wishlist):
        uow.wishlist_repository.add(wishlist)
        mediator.handle(
            AddWishlistItem(
                wishlist_uuid=wishlist.uuid,
                name="Apple",
                quantity=3,
                measurement_unit=MeasurementUnit.KILOGRAM,
                priority=Priority.LOW,
            )
        )
        assert len(wishlist.items) == 1

    def test_add_wishlist_item_non_existing_wishlist(self, mediator):
        with pytest.raises(WishlistNotFound):
            mediator.handle(
                AddWishlistItem(
                    wishlist_uuid=uuid.uuid4(),
                    name="Apple",
                    quantity=3,
                    measurement_unit=MeasurementUnit.KILOGRAM,
                    priority=Priority.LOW,
                )
            )


class TestRemoveWishlistItem:
    def test_remove_wishlist_item(self, mediator, uow, populated_wishlist):
        uow.wishlist_repository.add(populated_wishlist)
        item_to_remove = populated_wishlist.items[0]
        mediator.handle(
            RemoveWishlistItem(
                wishlist_uuid=populated_wishlist.uuid, item_uuid=item_to_remove.uuid
            )
        )
        assert item_to_remove not in populated_wishlist.items

    def test_remove_wishlist_item_non_existing_wishlist(self, mediator, apple_item):
        with pytest.raises(WishlistNotFound):
            mediator.handle(
                RemoveWishlistItem(
                    wishlist_uuid=uuid.uuid4(), item_uuid=apple_item.uuid
                )
            )

    def test_remove_wishlist_item_non_existing_wishlist_item(
        self, populated_wishlist, mediator, uow
    ):
        uow.wishlist_repository.add(populated_wishlist)
        with pytest.raises(WishlistItemNotFound):
            mediator.handle(
                RemoveWishlistItem(
                    wishlist_uuid=populated_wishlist.uuid, item_uuid=uuid.uuid4()
                )
            )


class TestMarkWishlistItemAsPurchased:
    def test_mark_wishlist_item_as_purchased(
        self, mediator, uow, populated_wishlist, apple_item
    ):
        uow.wishlist_repository.add(populated_wishlist)
        command = MarkWishlistItemAsPurchased(
            wishlist_uuid=populated_wishlist.uuid,
            item_uuid=apple_item.uuid,
        )

        mediator.handle(command)

        assert apple_item.is_purchased is True

    def test_already_purchased_wishlist_item(
        self, mediator, uow, populated_wishlist, purchased_banana_item
    ):
        uow.wishlist_repository.add(populated_wishlist)
        command = MarkWishlistItemAsPurchased(
            wishlist_uuid=populated_wishlist.uuid,
            item_uuid=purchased_banana_item.uuid,
        )

        with pytest.raises(WishlistItemAlreadyPurchased):
            mediator.handle(command)

    def test_non_existing_wishlist(self, mediator, apple_item):
        with pytest.raises(WishlistNotFound):
            mediator.handle(
                MarkWishlistItemAsPurchased(
                    wishlist_uuid=uuid.uuid4(),
                    item_uuid=apple_item.uuid,
                )
            )

    def test_non_existing_wishlist_item(self, mediator, uow, populated_wishlist):
        uow.wishlist_repository.add(populated_wishlist)
        with pytest.raises(WishlistItemNotFound):
            mediator.handle(
                MarkWishlistItemAsPurchased(
                    wishlist_uuid=populated_wishlist.uuid,
                    item_uuid=uuid.uuid4(),
                )
            )


class TestMarkWishlistItemAsNotPurchased:
    def test_mark_wishlist_item_as_not_purchased(
        self, mediator, uow, populated_wishlist, purchased_banana_item
    ):
        uow.wishlist_repository.add(populated_wishlist)
        command = MarkWishlistItemAsNotPurchased(
            wishlist_uuid=populated_wishlist.uuid,
            item_uuid=purchased_banana_item.uuid,
        )

        mediator.handle(command)

        assert purchased_banana_item.is_purchased is False

    def test_not_purchased_wishlist_item(
        self, mediator, uow, populated_wishlist, apple_item
    ):
        uow.wishlist_repository.add(populated_wishlist)
        command = MarkWishlistItemAsNotPurchased(
            wishlist_uuid=populated_wishlist.uuid,
            item_uuid=apple_item.uuid,
        )

        with pytest.raises(WishlistItemNotPurchased):
            mediator.handle(command)

    def test_non_existing_wishlist(self, mediator, apple_item):
        with pytest.raises(WishlistNotFound):
            mediator.handle(
                MarkWishlistItemAsNotPurchased(
                    wishlist_uuid=uuid.uuid4(),
                    item_uuid=apple_item.uuid,
                )
            )

    def test_non_existing_wishlist_item(self, mediator, uow, populated_wishlist):
        uow.wishlist_repository.add(populated_wishlist)
        command = MarkWishlistItemAsNotPurchased(
            wishlist_uuid=populated_wishlist.uuid,
            item_uuid=uuid.uuid4(),
        )

        with pytest.raises(WishlistItemNotFound):
            mediator.handle(command)


class TestArchiveWishlist:
    def test_archive_wishlist(self, mediator, uow, wishlist):
        uow.wishlist_repository.add(wishlist)
        mediator.handle(ArchiveWishlist(uuid=wishlist.uuid))
        assert wishlist.is_archived is True

    def test_archive_wishlist_non_existing_wishlist(self, mediator):
        with pytest.raises(WishlistNotFound):
            mediator.handle(ArchiveWishlist(uuid=uuid.uuid4()))

    def test_archive_wishlist_already_archived(self, mediator, uow, archived_wishlist):
        uow.wishlist_repository.add(archived_wishlist)
        with pytest.raises(WishlistAlreadyArchived):
            mediator.handle(ArchiveWishlist(uuid=archived_wishlist.uuid))

    def test_archive_wishlist_makes_it_private(self, mediator, uow, wishlist):
        wishlist.is_public = True
        uow.wishlist_repository.add(wishlist)
        mediator.handle(ArchiveWishlist(uuid=wishlist.uuid))
        assert wishlist.is_archived is True
        assert wishlist.is_public is False


class TestUnarchiveWishlist:
    def test_unarchive_wishlist(self, mediator, uow, archived_wishlist):
        uow.wishlist_repository.add(archived_wishlist)
        mediator.handle(UnarchiveWishlist(uuid=archived_wishlist.uuid))
        assert archived_wishlist.is_archived is False

    def test_unarchive_wishlist_non_existing_wishlist(self, mediator):
        with pytest.raises(WishlistNotFound):
            mediator.handle(UnarchiveWishlist(uuid=uuid.uuid4()))

    def test_unarchive_wishlist_not_archived(self, mediator, uow, wishlist):
        uow.wishlist_repository.add(wishlist)
        with pytest.raises(WishlistNotArchived):
            mediator.handle(UnarchiveWishlist(uuid=wishlist.uuid))


class TestChangeWishlistVisibility:
    def test_change_wishlist_visibility(self, mediator, uow, wishlist):
        uow.wishlist_repository.add(wishlist)
        assert wishlist.is_public is False
        mediator.handle(ChangeWishlistVisibility(uuid=wishlist.uuid, is_public=True))
        assert wishlist.is_public is True

    def test_change_wishlist_visibility_to_private(self, mediator, uow, wishlist):
        wishlist.is_public = True
        uow.wishlist_repository.add(wishlist)
        mediator.handle(ChangeWishlistVisibility(uuid=wishlist.uuid, is_public=False))
        assert wishlist.is_public is False

    def test_change_wishlist_visibility_non_existing_wishlist(self, mediator):
        with pytest.raises(WishlistNotFound):
            mediator.handle(ChangeWishlistVisibility(uuid=uuid.uuid4(), is_public=True))

    def test_change_wishlist_visibility_on_archived_rejected(
        self, mediator, uow, archived_wishlist
    ):
        uow.wishlist_repository.add(archived_wishlist)
        with pytest.raises(WishlistAlreadyArchived):
            mediator.handle(
                ChangeWishlistVisibility(uuid=archived_wishlist.uuid, is_public=True)
            )
