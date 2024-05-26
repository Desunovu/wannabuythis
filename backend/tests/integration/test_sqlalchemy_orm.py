def get_mapped_fields(domain_object) -> list[str]:
    """Get the list of mapped columns/relations after mapping"""
    columns = [field.name for field in domain_object.__mapper__.columns]
    relations = [field.key for field in domain_object.__mapper__.relationships]
    return columns + relations


def get_object_fields(domain_object) -> list[str]:
    """Get the list of object fields. Doesn't include fields starting with _ and events"""
    return [
        field
        for field in domain_object.__dict__
        if not field.startswith("_") and field != "events"
    ]


def check_fields_mapping(domain_object):
    """Check if all object fields are mapped field list"""
    object_fields = get_object_fields(domain_object)
    mapped_fields = get_mapped_fields(domain_object)
    for field in object_fields:
        assert field in mapped_fields, f"Field '{field}' is not mapped correctly"


class TestSQLAlchemyORM:
    def test_user_mapping(self, mappers, user):
        check_fields_mapping(domain_object=user)

    def test_wishlist_mapping(self, mappers, wishlist):
        check_fields_mapping(domain_object=wishlist)

    def test_wishlist_item_mapping(self, mappers, apple_item):
        check_fields_mapping(domain_object=apple_item)
