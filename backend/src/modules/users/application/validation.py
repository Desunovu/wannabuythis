from src.shared.application.exceptions import UserInvalidName
from src.shared.domain.username import Username


def validate_username(
    username: Username,
    min_length: int,
    max_length: int,
    forbidden_names: set[str],
):
    """Apply configurable username policy on top of the value object's rules."""

    if len(username) < min_length:
        raise UserInvalidName(
            f"Name is too short. Must be at least {min_length} characters long."
        )

    if len(username) > max_length:
        raise UserInvalidName(
            f"Name is too long. Must be no more than {max_length} characters long."
        )

    if username in {name.strip().casefold() for name in forbidden_names}:
        raise UserInvalidName(
            f"The name {username} is forbidden. Please choose a different name."
        )
