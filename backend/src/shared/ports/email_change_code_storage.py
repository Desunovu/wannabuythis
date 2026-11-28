import abc
from dataclasses import dataclass


@dataclass(frozen=True)
class PendingEmailChange:
    code: str
    new_email: str


class EmailChangeCodeStorage(abc.ABC):
    @abc.abstractmethod
    def get(self, username: str) -> PendingEmailChange | None:
        pass

    @abc.abstractmethod
    def save(self, username: str, code: str, new_email: str) -> None:
        pass

    @abc.abstractmethod
    def delete(self, username: str) -> None:
        pass


class FakeEmailChangeCodeStorage(EmailChangeCodeStorage):
    def __init__(self):
        self._pending: dict[str, PendingEmailChange] = {}

    def get(self, username: str) -> PendingEmailChange | None:
        return self._pending.get(username)

    def save(self, username: str, code: str, new_email: str) -> None:
        self._pending[username] = PendingEmailChange(code=code, new_email=new_email)

    def delete(self, username: str) -> None:
        self._pending.pop(username, None)
