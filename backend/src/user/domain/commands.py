from src.shared_kernel.commands import Command


class AddWishlist(Command):
    def __init__(self, user_id: int, wishlist_name: str):
        self.user_id = user_id
        self.wishlist_name = wishlist_name


class RemoveWishlist(Command):
    def __init__(self, wishlist_id: int):
        self.wishlist_id = wishlist_id
