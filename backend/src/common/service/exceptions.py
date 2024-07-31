from uuid import UUID


class ApplicationException(Exception):
    pass


class NotFoundException(ApplicationException):
    pass


class ConflictException(ApplicationException):
    pass


class ValidationException(ApplicationException):
    pass


class VerificationException(ApplicationException):
    pass


class Forbidden(ApplicationException):
    pass


class TokenException(ApplicationException):
    def __init__(self, message: str):
        super().__init__(message)


class UserNotAuthorized(Forbidden):
    def __init__(self, username: str):
        super().__init__(
            f"User '{username}' does not have permission to perform this action"
        )


class UserNotActive(Forbidden):
    def __init__(self, username: str):
        super().__init__(
            f"User {username} cannot perform this action because it is not active"
        )


class UserActive(Forbidden):
    def __init__(self, username: str):
        super().__init__(
            f"User {username} cannot perform this action because it is active"
        )


class UserNotFound(NotFoundException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' not found")


class UserExists(ConflictException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' exists")


class UserAlreadyActive(ConflictException):
    def __init__(self, username: str):
        super().__init__(f"User '{username}' is already active")


class UserAlreadyDeactivated(ConflictException):
    def __init__(self, username: str):
        super().__init__(f"User {username} is already deactivated")


class PasswordValidationError(ValidationException):
    def __init__(self, error_message: str = "Password validation failed"):
        super().__init__(error_message)


class PasswordVerificationError(VerificationException):
    def __init__(self, error_message: str = "Password does not match"):
        super().__init__(error_message)


class CodeVerificationError(VerificationException):
    def __init__(self, error_message: str = "Code does not match"):
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


class WishlistItemAlreadyPurchased(ConflictException):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist item '{uuid}' already purchased")


class WishlistItemNotPurchased(ConflictException):
    def __init__(self, uuid: UUID):
        super().__init__(f"Wishlist item '{uuid}' is not purchased")
