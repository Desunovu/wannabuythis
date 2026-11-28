from typing import Self

from src.shared.application.exceptions import UserInvalidName


def normalize_username(value: str) -> str:
    """The canonical lookup form of a username."""
    return value.strip().casefold()


class Username(str):
    """Canonical, validated username."""

    __slots__: tuple[str, ...] = ()

    def __new__(cls, value: object) -> Self:
        if not isinstance(value, str):
            raise UserInvalidName("Name must be a string")

        canonical = normalize_username(value)

        if not canonical:
            raise UserInvalidName("Name must not be empty.")

        if not canonical.isalnum():
            raise UserInvalidName("Name can only contain alphanumeric characters.")

        if not any(character.isalpha() for character in canonical):
            raise UserInvalidName("Name must contain at least one letter.")

        return super().__new__(cls, canonical)
