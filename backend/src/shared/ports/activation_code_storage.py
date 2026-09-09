import abc


class ActivationCodeStorage(abc.ABC):
    @abc.abstractmethod
    def get_activation_code(self, username: str) -> None | str:
        pass

    @abc.abstractmethod
    def save_activation_code(self, username: str, code: str) -> None:
        pass


class FakeActivationCodeStorage(ActivationCodeStorage):
    def __init__(self):
        self._activation_codes: dict[str, str] = {}

    def get_activation_code(self, username: str) -> None | str:
        return self._activation_codes.get(username)

    def save_activation_code(self, username: str, code: str) -> None:
        self._activation_codes[username] = code
