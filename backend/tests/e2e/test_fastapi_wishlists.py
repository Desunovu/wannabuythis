from src.wishlists.domain.model import MeasurementUnit, Priority

GET_WISHLIST_URL = "/wishlists"
GET_CURRENT_USER_WISHLISTS_URL = "/wishlists"
GET_WISHLIST_BY_USERNAME_URL = "/wishlists/user"
CREATE_WISHLIST_URL = "/wishlists/create"
CHANGE_WISHLIST_NAME_PATH = "/wishlists/change-name/"
ARCHIVE_WISHLIST_PATH = "/wishlists/archive/"
UNARCHIVE_WISHLIST_PATH = "/wishlists/unarchive/"
ADD_WISHLIST_ITEM_PATH = "/wishlists/add-item/"
REMOVE_WISHLIST_ITEM_PATH = "/wishlists/remove-item/"
MARK_WISHLIST_ITEM_AS_PURCHASED = "/wishlists/mark-item-as-purchased/"
MARK_WISHLIST_ITEM_AS_NOT_PURCHASED = "/wishlists/mark-item-as-not-purchased/"


class TestFastAPIWishlistsCommandRoutes:
    def test_create_wishlist(self, user_client):
        body = {"wishlist_name": "test wishlist"}
        response = user_client.post(url=CREATE_WISHLIST_URL, json=body)
        assert response.status_code == 200

    def test_change_wishlist_name(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{CHANGE_WISHLIST_NAME_PATH}{populated_wishlist.uuid}"
        body = {"new_name": "new test wishlist"}
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200

    def test_archive_wishlist(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{ARCHIVE_WISHLIST_PATH}{populated_wishlist.uuid}"
        response = user_with_populated_wishlist_client.post(url=url)
        assert response.status_code == 200

    def test_unarchive_wishlist(
        self, user_with_archived_wishlist_client, archived_wishlist
    ):
        url = f"{UNARCHIVE_WISHLIST_PATH}{archived_wishlist.uuid}"
        response = user_with_archived_wishlist_client.post(url=url)
        assert response.status_code == 200

    def test_add_wishlist_item(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{ADD_WISHLIST_ITEM_PATH}{populated_wishlist.uuid}"
        body = {
            "name": "test item",
            "quantity": 1,
            "measurement_unit": MeasurementUnit.PIECE,
            "priority": Priority.MEDIUM,
        }
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200

    def test_remove_wishlist_item(
        self, user_with_populated_wishlist_client, populated_wishlist, apple_item
    ):
        url = f"{REMOVE_WISHLIST_ITEM_PATH}{populated_wishlist.uuid}"
        body = {"item_uuid": apple_item.uuid.hex}
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200

    def test_mark_wishlist_item_as_purchased(
        self, user_with_populated_wishlist_client, populated_wishlist, apple_item
    ):
        url = f"{MARK_WISHLIST_ITEM_AS_PURCHASED}{populated_wishlist.uuid}"
        body = {"item_uuid": apple_item.uuid.hex}
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200

    def test_mark_wishlist_item_as_not_purchased(
        self,
        user_with_populated_wishlist_client,
        purchased_banana_item,
    ):
        url = f"{MARK_WISHLIST_ITEM_AS_NOT_PURCHASED}{purchased_banana_item.wishlist_uuid}"
        body = {"item_uuid": purchased_banana_item.uuid.hex}
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200


class TestFastAPIWishlistsQueryRoutes:
    def test_get_wishlist(self, client_with_populated_wishlist, populated_wishlist):
        url = f"{GET_WISHLIST_URL}/{populated_wishlist.uuid}"
        response = client_with_populated_wishlist.get(url)
        assert response.status_code == 200
        assert response.json()["name"] == populated_wishlist.name

    def test_get_current_user_wishlists(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        response = user_with_populated_wishlist_client.get(
            GET_CURRENT_USER_WISHLISTS_URL
        )
        assert response.status_code == 200
        assert response.json()[0]["name"] == populated_wishlist.name

    def test_get_wishlists_by_user(
        self, client_with_populated_wishlist, populated_wishlist
    ):
        url = f"{GET_WISHLIST_BY_USERNAME_URL}/{populated_wishlist.owner_username}"
        response = client_with_populated_wishlist.get(url)
        assert response.status_code == 200
        assert response.json()[0]["name"] == populated_wishlist.name
