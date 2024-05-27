from uuid import UUID


class UserNotFound(Exception):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' not found")


class UserExists(Exception):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists")


class UserAlreadyActive(Exception):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' is already active")


class UserNotActive(Exception):
    def __init__(self, username: str):
        super().__init__(f"User {username} is already deactivated")


class UserAlreadyHasRole(Exception):
    def __init__(self, username: str, role_name: str):
        super().__init__(f"User {username} already has role {role_name}")


class UserDoesNotHaveRole(Exception):
    def __init__(self, username: str, role_name: str):
        super().__init__(f"User {username} does not have role {role_name}")


class RoleNotFound(Exception):
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' not found")


class PasswordValidationError(Exception):
    def __init__(self, error_message: str = "Password validation failed"):
        super().__init__(error_message)


class PasswordVerificationError(Exception):
    def __init__(self, error_message: str = "Password does not match"):
        super().__init__(error_message)


class WishlistNotFound(Exception):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist '{uuid}' not found")


class WishlistItemNotFound(Exception):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist item '{uuid}' not found")


class WishlistAlreadyArchived(Exception):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist '{uuid}' already archived")


class WishlistNotArchived(Exception):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist '{uuid}' is not archived")
