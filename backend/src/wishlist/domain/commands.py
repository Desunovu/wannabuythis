class AddItem:
    def __init__(self, wishlist_id: int, name: str, quantity: int, measurement_unit: str):
        self.wishlist_id = wishlist_id
        self.name = name
        self.quantity = quantity
        self.measurement_unit = measurement_unit


class RemoveItem:
    def __init__(self, item_id: int):
        self.item_id = item_id
