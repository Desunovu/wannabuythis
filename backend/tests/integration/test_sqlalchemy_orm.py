import inspect

from src.users.domain import model as user_model
from src.wishlists.domain import model as wishlist_model


def get_mapper_columns_and_relationships(domain_class) -> list[str]:
    """Get the list of mapper columns/relationships"""
    columns = [field.name for field in domain_class.__mapper__.columns]
    relations = [field.key for field in domain_class.__mapper__.relationships]
    return columns + relations


def get_class_fields(domain_class) -> list[str]:
    """Get the list of class fields. Doesn't include events, as they are part of the aggregate"""
    return [
        name
        for name, value in inspect.getmembers(domain_class)
        if not name.startswith("_") and not inspect.isroutine(value) and name != "events"
    ]


def check_fields_mapping(domain_class):
    """Check if all class fields are in the mapper columns/relationships"""
    class_fields = get_class_fields(domain_class)
    mapped_fields = get_mapper_columns_and_relationships(domain_class)
    for field in class_fields:
        assert field in mapped_fields, f"Field '{field}' is not mapped correctly"


def check_classes_mapping(domain_classes: list):
    """Check if all class are mapped correctly"""
    for domain_class in domain_classes:
        check_fields_mapping(domain_class)


class TestUserContextClassMapping:
    def test_user_context_mapping(self, prepare_mappers):
        check_classes_mapping([user_model.User, user_model.Role, user_model.Permission])


class TestWishlistContextClassMapping:
    def test_wishlist_context_mapping(self, prepare_mappers):
        check_classes_mapping(
            [
                wishlist_model.Wishlist,
                wishlist_model.WishlistItem,
                wishlist_model.Priority,
                wishlist_model.MeasurementUnit,
            ]
        )
