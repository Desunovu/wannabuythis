from src.modules.wishlists.domain.model import MeasurementUnit, Priority
from tests.integration.conftest import add_wishlist_to_db

WISHLISTS_BASE_URL = "/wishlists"

GET_WISHLIST_BY_USERNAME_URL = f"{WISHLISTS_BASE_URL}/user"
CREATE_WISHLIST_URL = f"{WISHLISTS_BASE_URL}/create"
CHANGE_WISHLIST_NAME_URL = f"{WISHLISTS_BASE_URL}/change-name"
ARCHIVE_WISHLIST_URL = f"{WISHLISTS_BASE_URL}/archive"
UNARCHIVE_WISHLIST_URL = f"{WISHLISTS_BASE_URL}/unarchive"
SET_WISHLIST_VISIBILITY_URL = f"{WISHLISTS_BASE_URL}/set-visibility"
ADD_WISHLIST_ITEM_URL = f"{WISHLISTS_BASE_URL}/add-item"
REMOVE_WISHLIST_ITEM_URL = f"{WISHLISTS_BASE_URL}/remove-item"
MARK_WISHLIST_ITEM_AS_PURCHASED_URL = f"{WISHLISTS_BASE_URL}/mark-item-as-purchased"
MARK_WISHLIST_ITEM_AS_NOT_PURCHASED_URL = (
    f"{WISHLISTS_BASE_URL}/mark-item-as-not-purchased"
)
GET_ARCHIVED_WISHLISTS_URL = f"{WISHLISTS_BASE_URL}/archived"


class TestFastAPIWishlistsCommandRoutes:
    def test_create_private_wishlist(self, user_client):
        body = {"wishlist_name": "test wishlist", "is_public": False}
        response = user_client.post(url=CREATE_WISHLIST_URL, json=body)
        assert response.status_code == 200

    def test_create_wishlist_requires_visibility(self, user_client):
        body = {"wishlist_name": "test wishlist"}
        response = user_client.post(url=CREATE_WISHLIST_URL, json=body)
        assert response.status_code == 422

    def test_create_public_wishlist(self, user_client, client, user, wishlist_name):
        body = {"wishlist_name": wishlist_name, "is_public": True}
        response = user_client.post(url=CREATE_WISHLIST_URL, json=body)
        assert response.status_code == 200
        response = client.get(f"{GET_WISHLIST_BY_USERNAME_URL}/{user.username}")
        assert response.status_code == 200
        names = [entry["name"] for entry in response.json()]
        assert wishlist_name in names

    def test_change_wishlist_name(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{CHANGE_WISHLIST_NAME_URL}/{populated_wishlist.uuid}"
        body = {"new_name": "new test wishlist"}
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200

    def test_archive_wishlist(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{ARCHIVE_WISHLIST_URL}/{populated_wishlist.uuid}"
        response = user_with_populated_wishlist_client.post(url=url)
        assert response.status_code == 200

    def test_unarchive_wishlist(
        self, user_with_archived_wishlist_client, archived_wishlist
    ):
        url = f"{UNARCHIVE_WISHLIST_URL}/{archived_wishlist.uuid}"
        response = user_with_archived_wishlist_client.post(url=url)
        assert response.status_code == 200

    def test_add_wishlist_item(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{ADD_WISHLIST_ITEM_URL}/{populated_wishlist.uuid}"
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
        url = f"{REMOVE_WISHLIST_ITEM_URL}/{populated_wishlist.uuid}"
        body = {"item_uuid": apple_item.uuid.hex}
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200

    def test_mark_wishlist_item_as_purchased(
        self, user_with_populated_wishlist_client, populated_wishlist, apple_item
    ):
        url = f"{MARK_WISHLIST_ITEM_AS_PURCHASED_URL}/{populated_wishlist.uuid}"
        body = {"item_uuid": apple_item.uuid.hex}
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200

    def test_mark_wishlist_item_as_not_purchased(
        self,
        user_with_populated_wishlist_client,
        purchased_banana_item,
    ):
        url = f"{MARK_WISHLIST_ITEM_AS_NOT_PURCHASED_URL}/{purchased_banana_item.wishlist_uuid}"
        body = {"item_uuid": purchased_banana_item.uuid.hex}
        response = user_with_populated_wishlist_client.post(url=url, json=body)
        assert response.status_code == 200

    def test_set_wishlist_visibility(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{SET_WISHLIST_VISIBILITY_URL}/{populated_wishlist.uuid}"
        response = user_with_populated_wishlist_client.post(
            url=url, json={"is_public": True}
        )
        assert response.status_code == 200
        response = user_with_populated_wishlist_client.get(
            f"{WISHLISTS_BASE_URL}/{populated_wishlist.uuid}"
        )
        assert response.json()["is_public"] is True

    def test_set_wishlist_visibility_not_owner(
        self, client_with_user, second_user_client, populated_wishlist
    ):
        add_wishlist_to_db(client_with_user, populated_wishlist)
        url = f"{SET_WISHLIST_VISIBILITY_URL}/{populated_wishlist.uuid}"
        response = second_user_client.post(url=url, json={"is_public": True})
        assert response.status_code == 403

    def test_set_wishlist_visibility_on_archived_rejected(
        self, user_with_archived_wishlist_client, archived_wishlist
    ):
        url = f"{SET_WISHLIST_VISIBILITY_URL}/{archived_wishlist.uuid}"
        response = user_with_archived_wishlist_client.post(
            url=url, json={"is_public": True}
        )
        assert response.status_code == 409

    def test_archive_wishlist_makes_it_private(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{SET_WISHLIST_VISIBILITY_URL}/{populated_wishlist.uuid}"
        user_with_populated_wishlist_client.post(url=url, json={"is_public": True})
        user_with_populated_wishlist_client.post(
            f"{ARCHIVE_WISHLIST_URL}/{populated_wishlist.uuid}"
        )
        response = user_with_populated_wishlist_client.get(
            f"{WISHLISTS_BASE_URL}/{populated_wishlist.uuid}"
        )
        assert response.status_code == 200
        assert response.json()["is_public"] is False


class TestFastAPIWishlistsQueryRoutes:
    def test_get_public_wishlist(self, client_with_public_wishlist, public_wishlist):
        url = f"{WISHLISTS_BASE_URL}/{public_wishlist.uuid}"
        response = client_with_public_wishlist.get(url)
        assert response.status_code == 200
        assert response.json()["name"] == public_wishlist.name
        assert response.json()["is_public"] is True

    def test_get_private_wishlist_hidden_from_anonymous(
        self, client_with_populated_wishlist, populated_wishlist
    ):
        url = f"{WISHLISTS_BASE_URL}/{populated_wishlist.uuid}"
        response = client_with_populated_wishlist.get(url)
        assert response.status_code == 404

    def test_get_private_wishlist_by_owner(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        url = f"{WISHLISTS_BASE_URL}/{populated_wishlist.uuid}"
        response = user_with_populated_wishlist_client.get(url)
        assert response.status_code == 200
        assert response.json()["name"] == populated_wishlist.name

    def test_get_private_wishlist_hidden_from_authenticated_non_owner(
        self, client_with_user, second_user_client, populated_wishlist
    ):
        add_wishlist_to_db(client_with_user, populated_wishlist)
        url = f"{WISHLISTS_BASE_URL}/{populated_wishlist.uuid}"
        response = second_user_client.get(url)
        assert response.status_code == 404

    def test_get_public_wishlist_by_authenticated_non_owner(
        self, client_with_user, second_user_client, public_wishlist
    ):
        add_wishlist_to_db(client_with_user, public_wishlist)
        url = f"{WISHLISTS_BASE_URL}/{public_wishlist.uuid}"
        response = second_user_client.get(url)
        assert response.status_code == 200
        assert response.json()["is_public"] is True

    def test_get_archived_wishlist_hidden_from_anonymous(
        self, client_with_archived_wishlist, archived_wishlist
    ):
        url = f"{WISHLISTS_BASE_URL}/{archived_wishlist.uuid}"
        response = client_with_archived_wishlist.get(url)
        assert response.status_code == 404

    def test_get_archived_wishlist_by_owner(
        self, user_with_archived_wishlist_client, archived_wishlist
    ):
        url = f"{WISHLISTS_BASE_URL}/{archived_wishlist.uuid}"
        response = user_with_archived_wishlist_client.get(url)
        assert response.status_code == 200

    def test_get_wishlists_by_user(self, client_with_public_wishlist, public_wishlist):
        url = f"{GET_WISHLIST_BY_USERNAME_URL}/{public_wishlist.owner_username}"
        response = client_with_public_wishlist.get(url)
        assert response.status_code == 200
        names = [entry["name"] for entry in response.json()]
        assert public_wishlist.name in names

    def test_get_wishlists_by_user_public_only(
        self, client_with_user, public_wishlist, populated_wishlist
    ):
        populated_wishlist.name = "private wishlist"
        add_wishlist_to_db(client_with_user, public_wishlist)
        add_wishlist_to_db(client_with_user, populated_wishlist)
        response = client_with_user.get(
            f"{GET_WISHLIST_BY_USERNAME_URL}/{public_wishlist.owner_username}"
        )
        assert response.status_code == 200
        names = [entry["name"] for entry in response.json()]
        assert public_wishlist.name in names
        assert populated_wishlist.name not in names

    def test_get_current_user_wishlists(
        self, user_with_populated_wishlist_client, populated_wishlist
    ):
        response = user_with_populated_wishlist_client.get(WISHLISTS_BASE_URL)
        assert response.status_code == 200
        names = [entry["name"] for entry in response.json()]
        assert populated_wishlist.name in names

    def test_get_archived_wishlists(
        self, user_with_archived_wishlist_client, archived_wishlist
    ):
        response = user_with_archived_wishlist_client.get(GET_ARCHIVED_WISHLISTS_URL)
        assert response.status_code == 200
        names = [entry["name"] for entry in response.json()]
        assert archived_wishlist.name in names

    def test_get_archived_wishlists_requires_auth(self, client_with_archived_wishlist):
        response = client_with_archived_wishlist.get(GET_ARCHIVED_WISHLISTS_URL)
        assert response.status_code == 401
