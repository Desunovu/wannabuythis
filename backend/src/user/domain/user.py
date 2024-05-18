from src.shared_kernel.aggregates import AggregateRoot
from src.user.domain.events import PasswordChanged


class User(AggregateRoot):
    def __init__(self, username: str, email: str, password_hash: str):
        super().__init__()
        self.username = username
        self.email = email
        self.password_hash = password_hash

    # TODO add can_change_password method

    def change_password_hash(self, password_hash: str):
        self.password_hash = password_hash
        self.add_event(PasswordChanged(self.username))
