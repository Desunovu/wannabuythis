class UserNotFound(Exception):
    pass


class UserExists(Exception):
    pass


class UserAlreadyActive(Exception):
    pass


class UserNotActive(Exception):
    pass


class UserAlreadyHasRole(Exception):
    pass


class UserDoesNotHaveRole(Exception):
    pass


class RoleNotFound(Exception):
    pass


class PasswordValidationFailed(Exception):
    pass


class PasswordVerificationFailed(Exception):
    pass


class WishlistNotFound(Exception):
    pass


class WishlistItemNotFound(Exception):
    pass
