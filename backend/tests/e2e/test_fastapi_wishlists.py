GET_WISHLIST_URL = "/wishlists"
GET_CURRENT_USER_WISHLISTS_URL = "/wishlists"
GET_WISHLIST_BY_USERNAME_URL = "/wishlists/user"


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
