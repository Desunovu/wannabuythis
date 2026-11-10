import pytest

from src.shared.application.exceptions import UserInvalidName
from src.shared.domain.username import Username, normalize_username


@pytest.mark.parametrize(
    ("raw", "canonical"),
    [
        ("testuser", "testuser"),
        ("TestUser", "testuser"),
        ("  TestUser  ", "testuser"),
        # casefold() is deliberately used instead of lower().
        ("ß", "ss"),
    ],
)
def test_username_is_canonical_on_construction(raw, canonical):
    assert Username(raw) == canonical


@pytest.mark.parametrize("raw", ["", "   ", "user name", "user-name", "123"])
def test_username_rejects_invalid_values(raw):
    with pytest.raises(UserInvalidName):
        Username(raw)


def test_username_rejects_non_string():
    with pytest.raises(UserInvalidName):
        Username(123)


def test_username_is_idempotent():
    username = Username("  TestUser  ")
    assert Username(username) == username


def test_normalize_username_agrees_with_canonical_form():
    # Lookups normalize without validating, so both paths must agree.
    assert normalize_username("  TestUser  ") == Username("TestUser")
