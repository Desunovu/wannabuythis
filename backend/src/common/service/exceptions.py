from uuid import UUID

from fastapi.exceptions import ValidationException


class NotFoundException(Exception):
    pass


class ConflictException(Exception):
    pass


class VerificationException(Exception):
    pass


class Forbidden(Exception):
    pass


class UserNotActive(Forbidden):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' cannot sign in because of inactive status")


class UserNotFound(NotFoundException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' not found")


class UserExists(ConflictException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists")


class UserAlreadyActive(ConflictException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' is already active")


class UserAlreadyDeactivated(ConflictException):
    def __init__(self, username: str):
        super().__init__(f"User {username} is already deactivated")


class UserAlreadyHasRole(ConflictException):
    def __init__(self, username: str, role_name: str):
        super().__init__(f"User {username} already has role {role_name}")


class UserDoesNotHaveRole(ConflictException):
    def __init__(self, username: str, role_name: str):
        super().__init__(f"User {username} does not have role {role_name}")


class RoleNotFound(NotFoundException):
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' not found")


class PasswordValidationError(ValidationException):
    def __init__(self, error_message: str = "Password validation failed"):
        super().__init__(error_message)


class PasswordVerificationError(VerificationException):
    def __init__(self, error_message: str = "Password does not match"):
        super().__init__(error_message)


class WishlistNotFound(NotFoundException):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist '{uuid}' not found")


class WishlistItemNotFound(NotFoundException):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist item '{uuid}' not found")


class WishlistAlreadyArchived(ConflictException):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist '{uuid}' already archived")


class WishlistNotArchived(ConflictException):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist '{uuid}' is not archived")


class RoleAlreadyExists(ConflictException):
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' already exists")


class RoleAlreadyHasPermission(ConflictException):
    def __init__(self, role_name: str, permission_name: str):
        super().__init__(
            f"Role '{role_name}' already has permission '{permission_name}'"
        )


class RoleDoesNotHavePermission(Exception):
    def __init__(self, role_name: str, permission_name: str):
        super().__init__(
            f"Role '{role_name}' does not have permission '{permission_name}'"
        )
