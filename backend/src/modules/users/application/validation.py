from src.shared.application.exceptions import UserInvalidName


def validate_username(
    name: str,
    min_length: int,
    max_length: int,
    forbidden_names: set[str],
):
    if not isinstance(name, str):
        raise UserInvalidName("Name must be a string")

    if not name.isalnum():
        raise UserInvalidName("Name can only contain alphanumeric characters.")

    if not any(c.isalpha() for c in name):
        raise UserInvalidName("Name must contain at least one letter.")

    if len(name) < min_length:
        raise UserInvalidName(
            f"Name is too short. Must be at least {min_length} characters long."
        )

    if len(name) > max_length:
        raise UserInvalidName(
            f"Name is too long. Must be no more than {max_length} characters long."
        )

    if name.lower() in forbidden_names:
        raise UserInvalidName(
            f"The name {name} is forbidden. Please choose a different name."
        )
