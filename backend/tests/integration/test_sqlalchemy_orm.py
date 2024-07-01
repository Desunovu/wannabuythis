import inspect

from src.common.domain.aggregates import AggregateRoot
from src.common.domain.entities import Entity
from src.common.domain.value_objects import ValueObject
from src.roles.domain import model as role_model_module
from src.users.domain import model as user_model_module
from src.wishlists.domain import model as wishlist_model_module


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
        if not name.startswith("_")
        and not inspect.isroutine(value)
        and name != "events"
    ]


def check_fields_mapping(domain_class):
    """Check if all class fields are in the mapper columns/relationships"""
    class_fields = get_class_fields(domain_class)
    mapped_fields = get_mapper_columns_and_relationships(domain_class)
    for field in class_fields:
        assert field in mapped_fields, f"Field '{field}' is not mapped correctly"


def discover_classes(module):
    """Discover all domain classes in the given module"""
    members = inspect.getmembers(module)
    classes = [
        member[1]
        for member in members
        if inspect.isclass(member[1])
        and member[1].__module__ == module.__name__
        and issubclass(member[1], (AggregateRoot, Entity, ValueObject))
    ]
    return classes


def check_module_classes_mapping(module):
    """Check if all module classes are mapped correctly"""
    for domain_class in discover_classes(module):
        check_fields_mapping(domain_class)


class TestUserContextClassMapping:
    def test_user_context_mapping(self, prepare_mappers):
        check_module_classes_mapping(user_model_module)


class TestWishlistContextClassMapping:
    def test_wishlist_context_mapping(self, prepare_mappers):
        check_module_classes_mapping(wishlist_model_module)


class TestRoleContextClassMapping:
    def test_role_context_mapping(self, prepare_mappers):
        check_module_classes_mapping(role_model_module)
