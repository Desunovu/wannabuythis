import abc


class ActivationCodeStorage(abc.ABC):
    @abc.abstractmethod
    def get_activation_code(self, username: str) -> str:
        pass

    @abc.abstractmethod
    def save_activation_code(self, username: str, code: str) -> None:
        pass
