from src.user.domain.events import WishlistAdded, WishlistRemoved, WishlistNotFound


def test_user_can_add_wishlist(user, wishlist):
    """Test that a user can add a wishlist and that the WishlistAdded event is published"""
    user.add_wishlist(wishlist)

    assert wishlist in user.wishlists
    assert user.events[-1] == WishlistAdded(user.id, wishlist.id)


def test_user_can_remove_wishlist(user_with_wishlists):
    """Test that a user can remove a wishlist and that the WishlistRemoved event is published"""
    wishlist = user_with_wishlists.wishlists[0]
    user_with_wishlists.remove_wishlist(wishlist.id)

    assert wishlist not in user_with_wishlists.wishlists
    assert user_with_wishlists.events[-1] == WishlistRemoved(
        user_with_wishlists.id, wishlist.id
    )


def test_user_cannot_remove_wishlist(user_with_wishlists):
    """
    Test that WishlistNotFound event is published and nothing else happens  if a user tries to remove a non-existing wishlist
    """
    wishlists_copy = user_with_wishlists.wishlists[:]
    user_with_wishlists.remove_wishlist(999)

    assert wishlists_copy == user_with_wishlists.wishlists
    assert user_with_wishlists.events[-1] == WishlistNotFound(
        user_with_wishlists.id, 999
    )
